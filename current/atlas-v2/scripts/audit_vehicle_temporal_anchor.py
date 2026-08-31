"""Audit whether editorial vehicles can be placed in time, and build the remediation queue.

D-002 puts the vehicle at the centre of the Atlas, but every projection of the
product is temporal: the timeline, the annual chapter, the period bundles and the
specialised views all filter by year. A vehicle without a dated claim therefore
exists in the acervo and is unreachable in the product.

This audit produces the CP24 worklist. A vehicle leaves the queue when it has a
dated claim with a source *and* at least one source outside the interested party,
so a single editorial pass closes both the temporal anchor and the independence
debt for that record.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from source_resolution import resolve as resolve_source_types

ROOT = Path(__file__).resolve().parents[1]
CLASSIFICATION = ROOT / "content/source-classification.json"
REGISTRY = ROOT / "migration/sources.jsonld"
BASELINE = ROOT / "gates/editorial-baseline.json"
DEFAULT_REPORT = ROOT / "reports" / "vehicle-temporal-anchor.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def year(value: object) -> int | None:
    match = re.match(r"^(\d{4})", str(value or ""))
    return int(match.group(1)) if match else None


def claim_years(document: dict) -> list[int]:
    """Years a claim actually asserts, by the same reading the coverage audit uses."""
    years: set[int] = set()
    for claim in document.get("claims") or []:
        validity = claim.get("validity") or {}
        for bound in (validity.get("from"), validity.get("until")):
            if parsed := year(bound):
                years.add(parsed)
        obj = claim.get("object")
        if isinstance(obj, dict) and obj.get("type") == "date":
            if parsed := year(obj.get("value")):
                years.add(parsed)
    return sorted(years)


def corpora() -> tuple[dict[str, dict], dict[str, dict], dict[str, dict]]:
    migrated = {}
    for path in sorted((ROOT / "migration/entities").glob("*.jsonld")):
        document = load(path)
        migrated[document["id"]] = document
    authored = {}
    for path in sorted((ROOT / "content/entities").glob("*.jsonld")):
        document = load(path)
        authored[document["id"]] = document
    # Mirror build_bundles.py: the two corpora are merged, not chosen between.
    published = dict(migrated)
    for entity_id, document in authored.items():
        published[entity_id] = merge_entity(migrated[entity_id], document) if entity_id in migrated else document
    return migrated, authored, published


def merge_entity(migrated: dict, authored: dict) -> dict:
    """Union two documents describing the same identity.

    Five identities exist in both corpora, and the two halves are complementary:
    the migrated document carries the relational claims (who engineered it, which
    component it uses, who manufactured it) while the authored document carries
    the temporal ones and the per-document sources. Deferring to either side
    discarded sourced facts — the Porsche 917 lost its engineer and its engine,
    or else its 1969 dates — so the build keeps both. content/entities is the
    authority for shared fields; migration-only claims are preserved.
    """
    merged = {**migrated, **authored}
    authored_claims = authored.get("claims") or []
    known = {claim["id"] for claim in authored_claims}
    inherited = [claim for claim in migrated.get("claims") or [] if claim["id"] not in known]
    merged["claims"] = sorted(authored_claims + inherited, key=lambda claim: claim["id"])
    return merged

def audit() -> dict:
    classification = load(CLASSIFICATION)
    dependent = set(classification["dependentSourceTypes"])
    migrated, authored, published = corpora()
    resolved, _ = resolve_source_types(classification, list(migrated.values()) + list(authored.values()))

    queue: list[dict] = []
    anchored: list[str] = []
    discarded_anchor: list[dict] = []

    for entity_id, document in sorted(published.items()):
        metadata = document.get("metadata") or {}
        if document.get("type") != "Vehicle" or metadata.get("editorial_level") != "editorial":
            continue
        years = claim_years(document)
        types = {resolved.get(source_id) for claim in document.get("claims") or [] for source_id in claim.get("sources") or []}
        confrontable = any(source_type and source_type not in dependent for source_type in types)

        # A dated claim may already exist in a document the build discards. That
        # is a build defect, not editorial work, and must not enter the research
        # queue disguised as missing evidence.
        alternate = authored.get(entity_id) if published[entity_id] is not authored.get(entity_id) else None
        alternate_years = claim_years(alternate) if alternate else []
        if not years and alternate_years:
            discarded_anchor.append({
                "id": entity_id,
                "name": document.get("name"),
                "yearsInDiscardedDocument": alternate_years,
            })

        if years and confrontable:
            anchored.append(entity_id)
        else:
            queue.append({
                "id": entity_id,
                "name": document.get("name"),
                "needsTemporalAnchor": not years,
                "needsIndependentSource": not confrontable,
                "claimCount": len(document.get("claims") or []),
                "assertedYears": years,
            })

    audited = len(anchored) + len(queue)
    baseline = load(BASELINE) if BASELINE.is_file() else {"maximums": {}, "minimums": {}}
    floor = baseline.get("minimums", {}).get("anchoredVehicles")
    errors: list[str] = []
    if floor is not None and len(anchored) < floor:
        errors.append(f"anchored vehicles regressed: {len(anchored)} now, baseline requires {floor}")

    report = {
        "version": "1.0.0",
        "status": "PASS" if not errors else "FAIL",
        "summary": {
            "editorialVehicles": audited,
            "anchoredVehicles": len(anchored),
            "queuedVehicles": len(queue),
            "needingTemporalAnchor": sum(item["needsTemporalAnchor"] for item in queue),
            "needingIndependentSource": sum(item["needsIndependentSource"] for item in queue),
            "needingBoth": sum(item["needsTemporalAnchor"] and item["needsIndependentSource"] for item in queue),
            "anchorHeldInDiscardedDocument": len(discarded_anchor),
        },
        "baseline": {"anchoredVehiclesFloor": floor},
        "anchorHeldInDiscardedDocument": discarded_anchor,
        "queue": queue,
        "errors": errors,
    }
    canonical = json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    report["reportSha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--check", action="store_true", help="Compare generated report with the versioned report")
    parser.add_argument("--promote", action="store_true", help="Tighten the ratchet to the observed values")
    args = parser.parse_args()
    report = audit()

    if args.promote:
        baseline = load(BASELINE) if BASELINE.is_file() else {"version": "1.0.0"}
        baseline.setdefault("minimums", {})["anchoredVehicles"] = report["summary"]["anchoredVehicles"]
        dump(BASELINE, baseline)
        report = audit()

    if args.check:
        if not args.output.is_file() or load(args.output) != report:
            raise SystemExit("vehicle temporal anchor report is stale; regenerate it")
    else:
        dump(args.output, report)

    print(json.dumps({"status": report["status"], **report["summary"]}, ensure_ascii=False, sort_keys=True))
    if report["status"] != "PASS":
        raise SystemExit("\n".join(report["errors"]))


if __name__ == "__main__":
    main()
