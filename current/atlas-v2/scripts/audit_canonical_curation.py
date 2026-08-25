"""Reconcile the legacy candidate census with Atlas v2 canonical entities."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY_DATA = ROOT.parent / "atlas-web" / "data"
DECISIONS = ROOT / "content" / "canonical-curation-decisions.json"
REPORT = ROOT / "reports" / "canonical-curation.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def build() -> tuple[dict, dict]:
    brands = read_csv(LEGACY_DATA / "brand.candidates.csv")
    historical = read_csv(LEGACY_DATA / "historical-significance.candidates.csv")
    entity_docs = [load(path) for path in sorted((ROOT / "migration" / "entities").glob("*.jsonld"))]
    by_legacy = {
        entity.get("legacy", {}).get("id"): entity
        for entity in entity_docs
        if entity.get("legacy", {}).get("id")
    }

    inputs: list[dict[str, str]] = []
    for row in brands:
        inputs.append({**row, "candidateClass": "brand"})
    for row in historical:
        inputs.append({**row, "candidateClass": "historical"})

    duplicate_ids = sorted(
        legacy_id for legacy_id, count in Counter(row["entity_id"] for row in inputs if row["entity_id"]).items()
        if count > 1
    )
    missing_entities: list[str] = []
    queue: list[dict] = []
    terminal: list[dict] = []

    for row in sorted(inputs, key=lambda item: (item["candidateClass"], item["candidate_name"].casefold())):
        legacy_id = row.get("entity_id", "")
        entity = by_legacy.get(legacy_id) if legacy_id else None
        if legacy_id and not entity:
            missing_entities.append(legacy_id)
        claims = entity.get("claims", []) if entity else []
        evidence_complete = bool(claims) and all(claim.get("sources") and claim.get("evidence") for claim in claims)
        metadata = entity.get("metadata", {}) if entity else {}
        source_backed = evidence_complete and metadata.get("verification_state") == "source_backed"
        item = {
            "candidateClass": row["candidateClass"],
            "candidateName": row["candidate_name"],
            "canonicalId": entity.get("id") if entity else None,
            "legacyId": legacy_id or None,
            "legacyDecision": row["decision"],
            "claimCount": len(claims),
            "editorialLevel": metadata.get("editorial_level", "unmigrated"),
            "evidenceState": "source-backed" if source_backed else "identity-only",
        }
        if row["candidateClass"] == "brand":
            item.update({"wave": row["wave"], "scopeLevel": row["scope_level"], "region": row["region_cluster"]})
        else:
            item.update({"year": int(row["year"]), "kind": row["kind"], "associatedBrand": row["associated_brand"]})

        if row["decision"] == "cataloged":
            item["curationState"] = "ready-for-editorial-review" if source_backed else "needs-individual-source"
            queue.append(item)
        else:
            item["curationState"] = "legacy-decision-preserved"
            terminal.append(item)

    if len(queue) != 522:
        raise ValueError(f"canonical queue drift: expected 522, got {len(queue)}")
    if duplicate_ids or missing_entities:
        raise ValueError(f"candidate identity failure: duplicates={duplicate_ids}, missing={missing_entities}")

    queue_counts = Counter(item["curationState"] for item in queue)
    class_counts = Counter(item["candidateClass"] for item in queue)
    terminal_counts = Counter(item["legacyDecision"] for item in terminal)
    decisions = {
        "version": "2.0.0",
        "policy": {
            "cataloged": "Permanece pesquisável, mas só é promovido após fonte individual, evidência e revisão editorial.",
            "published": "Decisão editorial anterior preservada e sujeita à auditoria semântica regular.",
            "context_only": "Mantido apenas como contexto; não promove entidade sem nova decisão documentada.",
            "hold": "Mantido em espera explícita; não é promovido automaticamente.",
        },
        "queue": queue,
        "terminalLegacyDecisions": terminal,
    }
    decision_text = canonical(decisions)
    report = {
        "status": "PASS",
        "candidateInputs": len(inputs),
        "canonicalQueue": len(queue),
        "queueByClass": dict(sorted(class_counts.items())),
        "queueByState": dict(sorted(queue_counts.items())),
        "terminalLegacyDecisions": dict(sorted(terminal_counts.items())),
        "duplicateLegacyIds": len(duplicate_ids),
        "missingMigratedEntities": len(missing_entities),
        "decisionsSha256": hashlib.sha256(decision_text.encode()).hexdigest(),
    }
    return decisions, report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    decisions, report = build()
    expected_decisions = canonical(decisions)
    expected_report = canonical(report)
    if args.check:
        if not DECISIONS.exists() or DECISIONS.read_text(encoding="utf-8") != expected_decisions:
            raise SystemExit("canonical curation decisions are stale")
        if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != expected_report:
            raise SystemExit("canonical curation report is stale")
    else:
        DECISIONS.write_text(expected_decisions, encoding="utf-8")
        REPORT.write_text(expected_report, encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
