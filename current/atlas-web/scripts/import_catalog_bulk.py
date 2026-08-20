#!/usr/bin/env python3
"""Import the Atlas-curated mass catalog without promoting records to editorial claims."""
from __future__ import annotations

import csv
import json
import sqlite3
from collections import Counter
from pathlib import Path

from enrich_people_batch_01 import stable_uuid7

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[1]
DB = ROOT / "data" / "atlas.sqlite"
BRANDS = ROOT / "data" / "brand.candidates.csv"
SIGNIFICANCE = ROOT / "data" / "historical-significance.candidates.csv"
SNAPSHOT_DIR = ROOT / "data" / "imports" / "atlas-curation"
REPORT = WORKSPACE / "handoff" / "MASS_CATALOG_IMPORT.md"
NOW = "2026-08-20T12:00:00+00:00"


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def insert_entity(db: sqlite3.Connection, name: str, entity_type: str, description: str, metadata: dict, scheme: str, value: str) -> tuple[str, bool]:
    existing = db.execute("SELECT id FROM entity WHERE canonical_name=? COLLATE NOCASE AND entity_type=?", (name, entity_type)).fetchone()
    if existing:
        current = db.execute("SELECT metadata_json FROM entity WHERE id=?", (existing[0],)).fetchone()
        current_metadata = json.loads(current[0] or "{}")
        if current_metadata.get("editorial_level") == "catalog" and current_metadata.get("verification_state") != "source_backed":
            db.execute("UPDATE entity SET description=?,metadata_json=?,updated_at=? WHERE id=?", (description, json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, existing[0]))
        db.execute(
            "INSERT OR IGNORE INTO external_identifier(id,entity_id,scheme,value,url,created_at) VALUES(?,?,?,?,NULL,?)",
            (stable_uuid7(f"external:{scheme}:{value}"), existing[0], scheme, value, NOW),
        )
        return existing[0], False
    entity_id = stable_uuid7(f"entity:{name}")
    if db.execute("SELECT 1 FROM entity WHERE id=?", (entity_id,)).fetchone():
        entity_id = stable_uuid7(f"entity:{entity_type}:{name}")
    db.execute(
        """INSERT INTO entity(id,entity_type,canonical_name,slug,description,metadata_json,created_at,updated_at)
           VALUES(?,?,?,NULL,?,?,?,?)""",
        (entity_id, entity_type, name, description, json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, NOW),
    )
    db.execute(
        """INSERT OR IGNORE INTO external_identifier(id,entity_id,scheme,value,url,created_at)
           VALUES(?,?,?,?,NULL,?)""",
        (stable_uuid7(f"external:{scheme}:{value}"), entity_id, scheme, value, NOW),
    )
    return entity_id, True


def main() -> int:
    brands = load_csv(BRANDS)
    candidates = load_csv(SIGNIFICANCE)
    db = sqlite3.connect(DB)
    db.execute("PRAGMA foreign_keys=ON")
    created = Counter()
    try:
        # Existing publication-quality entities retain their requirements explicitly.
        for entity_id, raw in db.execute("SELECT id,metadata_json FROM entity"):
            metadata = json.loads(raw or "{}")
            if not metadata.get("editorial_level"):
                metadata["editorial_level"] = "editorial"
                db.execute("UPDATE entity SET metadata_json=?,updated_at=? WHERE id=?", (json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, entity_id))

        for row in brands:
            if row["decision"] not in {"needs_research", "cataloged"}:
                continue
            name = row["candidate_name"].strip()
            entity_id, was_created = insert_entity(
                db,
                name,
                "brand",
                f"Registro catalográfico de {name}, incluído no censo global M01–M12 do Atlas. A história corporativa, os períodos de atividade e os modelos associados ainda aguardam aprofundamento editorial e fontes individuais.",
                {"editorial_level": "catalog", "editorial_batch": "MASS01", "catalog_source": "atlas-brand-census", "wave": row["wave"], "region_cluster": row["region_cluster"], "brand_status": "em pesquisa", "relevance_score": 35, "promotion_state": "queued"},
                "atlas-brand-census",
                f"{row['wave']}:{name}",
            )
            row["decision"] = "cataloged"
            row["entity_id"] = entity_id
            row["notes"] = "Registro catalográfico importado no lote MASS01; aprofundamento editorial pendente."
            created["brand"] += int(was_created)

        for row in candidates:
            if row["decision"] not in {"include_candidate", "cataloged"}:
                continue
            name = row["candidate_name"].strip()
            entity_id, was_created = insert_entity(
                db,
                name,
                "vehicle",
                f"Registro catalográfico de {name} ({row['year']}), selecionado pelo Atlas por sua possível contribuição histórica em {row['contribution_tracks'].replace('|', ', ')}. O verbete aguarda documentação individual antes da promoção editorial.",
                {"editorial_level": "catalog", "editorial_batch": "MASS01", "catalog_source": "atlas-significance-candidates", "candidate_kind": row["kind"], "candidate_year": int(row["year"]), "associated_brand": row["associated_brand"], "contribution_tracks": row["contribution_tracks"].split("|"), "relevance_score": min(100, 40 + 10 * len(row["contribution_tracks"].split("|")) + (5 if row["kind"] in {"prototype_program", "one_off"} else 0)), "promotion_state": "priority_editorial"},
                "atlas-significance-candidate",
                f"{row['kind']}:{row['year']}:{name}",
            )
            row["decision"] = "cataloged"
            row["entity_id"] = entity_id
            created["vehicle"] += int(was_created)

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    write_csv(BRANDS, brands)
    write_csv(SIGNIFICANCE, candidates)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    (SNAPSHOT_DIR / "brand-census.snapshot.json").write_text(json.dumps(brands, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SNAPSHOT_DIR / "historical-candidates.snapshot.json").write_text(json.dumps(candidates, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(created.values())
    with sqlite3.connect(DB) as report_db:
        catalog_totals = dict(
            report_db.execute(
                """SELECT entity_type, COUNT(*)
                   FROM entity
                   WHERE json_extract(metadata_json, '$.editorial_batch') = 'MASS01'
                   GROUP BY entity_type"""
            ).fetchall()
        )
    catalog_total = sum(catalog_totals.values())
    REPORT.write_text(
        "# Importação catalográfica MASS01\n\n"
        "Data: 2026-08-20\n\n"
        "Política: registros catalográficos são pesquisáveis, atribuídos e não equivalem a claims históricos verificados.\n\n"
        f"- Acervo consolidado do lote: **{catalog_total}** registros "
        f"(**{catalog_totals.get('brand', 0)}** marcas e **{catalog_totals.get('vehicle', 0)}** veículos).\n"
        f"- Nesta execução: **{total}** novos registros "
        f"(**{created['brand']}** marcas e **{created['vehicle']}** veículos).\n"
        "- Fonte do lote: registros de curadoria M01–M12 e candidatos de relevância histórica do próprio Atlas.\n"
        "- Mídia obrigatória: não, até promoção editorial.\n"
        "- Evidência obrigatória: antes de promoção para `editorial`.\n",
        encoding="utf-8",
    )
    print(json.dumps({"created": dict(created), "total_created": total, "brands": len(brands), "historical_candidates": len(candidates)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
