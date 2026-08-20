from __future__ import annotations

import csv
import json
import sqlite3
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[1]
DB = ROOT / "data" / "atlas.sqlite"
CRITERIA = ROOT / "data" / "editorial-completeness.criteria.json"
CSV_OUTPUT = WORKSPACE / "handoff" / "EDITORIAL_COMPLETENESS_BACKLOG.csv"
REPORT_OUTPUT = WORKSPACE / "handoff" / "EDITORIAL_COMPLETENESS_REPORT.md"


def word_count(value: str | None) -> int:
    return len((value or "").split())


def main() -> int:
    criteria = json.loads(CRITERIA.read_text(encoding="utf-8"))
    global_rules = criteria["global"]
    weights = global_rules["weights"]
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    entities = db.execute(
        """
        SELECT e.*,
               COALESCE(s.statement_count, 0) AS statement_count,
               COALESCE(s.evidenced_count, 0) AS evidenced_count
        FROM entity e
        LEFT JOIN (
          SELECT linked.entity_id,
                 COUNT(DISTINCT linked.statement_id) AS statement_count,
                 COUNT(DISTINCT CASE WHEN ce.evidence_id IS NOT NULL THEN linked.statement_id END) AS evidenced_count
          FROM (
            SELECT id AS statement_id, subject_entity_id AS entity_id FROM statement
            UNION ALL
            SELECT id AS statement_id, object_entity_id AS entity_id FROM statement WHERE object_entity_id IS NOT NULL
          ) linked
          LEFT JOIN claim c ON c.statement_id = linked.statement_id
          LEFT JOIN claim_evidence ce ON ce.claim_id = c.id
          GROUP BY linked.entity_id
        ) s ON s.entity_id = e.id
        ORDER BY e.entity_type, e.canonical_name, e.id
        """
    ).fetchall()

    rows: list[dict[str, object]] = []
    for entity in entities:
        type_rules = criteria["types"][entity["entity_type"]]
        metadata = json.loads(entity["metadata_json"] or "{}")
        description_words = word_count(entity["description"])
        editorial_level = metadata.get("editorial_level", "editorial")
        if editorial_level == "catalog":
            rows.append(
                {
                    "priority": "P4",
                    "status": "catalog",
                    "score": 0,
                    "entity_id": entity["id"],
                    "entity_type": entity["entity_type"],
                    "canonical_name": entity["canonical_name"],
                    "description_words": description_words,
                    "connected_statements": entity["statement_count"],
                    "required_statements": type_rules["minimum_connected_statements"],
                    "evidenced_statements": entity["evidenced_count"],
                    "gaps": "editorial_promotion_required",
                }
            )
            continue
        description_ok = description_words >= global_rules["minimum_description_words"]
        statements_required = type_rules["minimum_connected_statements"]
        statements_ok = entity["statement_count"] >= statements_required
        evidence_ok = entity["statement_count"] > 0 and entity["evidenced_count"] == entity["statement_count"]
        missing_metadata = [key for key in type_rules["required_metadata"] if metadata.get(key) in (None, "", [])]
        metadata_ok = not missing_metadata
        score = (
            weights["description"] * int(description_ok)
            + weights["connected_statements"] * min(entity["statement_count"] / statements_required, 1)
            + weights["evidence"] * int(evidence_ok)
            + weights["type_metadata"] * int(metadata_ok)
        )
        score = round(score, 1)
        if score >= criteria["thresholds"]["complete"]:
            status = "complete"
        elif score >= criteria["thresholds"]["substantial"]:
            status = "substantial"
        elif score >= criteria["thresholds"]["partial"]:
            status = "partial"
        else:
            status = "stub"
        gaps: list[str] = []
        if not description_ok:
            gaps.append(f"description<{global_rules['minimum_description_words']}_words")
        if not statements_ok:
            gaps.append(f"connected_statements<{statements_required}")
        if not evidence_ok:
            gaps.append("connected_statements_without_full_evidence")
        gaps.extend(f"metadata:{key}" for key in missing_metadata)
        priority = "P0" if status == "stub" else "P1" if status == "partial" else "P2" if status == "substantial" else "P3"
        rows.append(
            {
                "priority": priority,
                "status": status,
                "score": score,
                "entity_id": entity["id"],
                "entity_type": entity["entity_type"],
                "canonical_name": entity["canonical_name"],
                "description_words": description_words,
                "connected_statements": entity["statement_count"],
                "required_statements": statements_required,
                "evidenced_statements": entity["evidenced_count"],
                "gaps": "|".join(gaps),
            }
        )
    db.close()

    fieldnames = list(rows[0])
    with CSV_OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    statuses = Counter(str(row["status"]) for row in rows)
    priorities = Counter(str(row["priority"]) for row in rows)
    type_rows: list[str] = []
    for entity_type in sorted({str(row["entity_type"]) for row in rows}):
        subset = [row for row in rows if row["entity_type"] == entity_type]
        complete = sum(row["status"] == "complete" for row in subset)
        average = sum(float(row["score"]) for row in subset) / len(subset)
        type_rows.append(f"| {entity_type} | {len(subset)} | {complete} | {average:.1f} |")

    report = f"""# Auditoria de completude editorial

Data: 2026-08-18  
Critérios: `current/atlas-web/data/editorial-completeness.criteria.json`  
Backlog: `handoff/EDITORIAL_COMPLETENESS_BACKLOG.csv`

## Resultado

- Entidades auditadas: **{len(rows)}**
- Completas: **{statuses['complete']}**
- Substanciais: **{statuses['substantial']}**
- Parciais: **{statuses['partial']}**
- Stubs: **{statuses['stub']}**
- Catalogadas: **{statuses['catalog']}**
- Prioridade P0: **{priorities['P0']}**
- Prioridade P1: **{priorities['P1']}**

Este resultado substitui qualquer interpretação anterior de que cobertura de rota ou de mídia equivalia a completude editorial.

## Por tipo

| Tipo | Entidades | Completas | Nota média |
|---|---:|---:|---:|
{chr(10).join(type_rows)}

## Definição operacional

Uma entidade somente recebe 100 pontos quando possui descrição contextual de pelo menos {global_rules['minimum_description_words']} palavras, o mínimo de statements do seu tipo, evidência para todos esses statements e metadados estruturais obrigatórios. A matriz é um piso editorial auditável, não uma promessa de exaustividade universal.
"""
    REPORT_OUTPUT.write_text(report, encoding="utf-8")
    print(json.dumps({"entities": len(rows), "statuses": statuses, "priorities": priorities}, ensure_ascii=False, default=dict))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
