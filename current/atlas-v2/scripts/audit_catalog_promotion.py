"""Audit the boundary between catalogued identity and editorial entity.

The census preserved 522 automotive identities so they would not vanish from the
acervo. Preserving an identity is not the same as publishing knowledge about it,
and the two were indistinguishable in the product until the editorial level
reached the interface.

The promotion bar is deliberately low and deliberately not zero: at least one
claim carrying evidence, and at least one source outside the interested party.
It asks for a checkable fact, not a complete history.

The audit reports two queues. Catalogued identities that already clear the bar
should be promoted; entities already marked editorial that do not clear it are
declared debt under a ratchet, so the corpus can be remediated in batches while
new work has to arrive above the bar.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from source_resolution import resolve as resolve_source_types

ROOT = Path(__file__).resolve().parents[1]
CLASSIFICATION = ROOT / "content/source-classification.json"
REGISTRY = ROOT / "migration/sources.jsonld"
BASELINE = ROOT / "gates/editorial-baseline.json"
DEFAULT_REPORT = ROOT / "reports" / "catalog-promotion.json"

# Wikipedia and Wikidata carry sourceType "reference". They are independent of
# the manufacturer and therefore satisfy the bar, but an entity resting on them
# alone is a weaker record than one backed by an archive, a museum or a
# regulator. The count is reported so the distinction stays visible.
REFERENCE_TYPES = {"reference", "structured_reference", "structured_data"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def published_entities() -> list[dict]:
    """Mirror build_bundles.py: content/entities is the authority and wins."""
    by_id: dict[str, dict] = {}
    for path in sorted((ROOT / "migration/entities").glob("*.jsonld")):
        document = load(path)
        by_id[document["id"]] = document
    for path in sorted((ROOT / "content/entities").glob("*.jsonld")):
        document = load(path)
        if existing := by_id.get(document["id"]):
            document = merge_entity(existing, document)
        by_id[document["id"]] = document
    return list(by_id.values())


def evaluate(document: dict, resolved: dict[str, str], dependent: set[str]) -> dict:
    claims = document.get("claims") or []
    evidenced = [claim for claim in claims if claim.get("evidence") and claim.get("sources")]
    types = {resolved.get(source_id) for claim in claims for source_id in claim.get("sources") or []}
    types.discard(None)
    independent = {kind for kind in types if kind not in dependent}
    return {
        "id": document["id"],
        "name": document.get("name"),
        "type": document.get("type"),
        "claimCount": len(claims),
        "evidencedClaimCount": len(evidenced),
        "hasEvidencedClaim": bool(evidenced),
        "hasIndependentSource": bool(independent),
        "independentOnlyByReference": bool(independent) and independent <= REFERENCE_TYPES,
        "clearsBar": bool(evidenced) and bool(independent),
    }



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
    documents = [load(path) for path in
                 list((ROOT / "migration/entities").glob("*.jsonld"))
                 + list((ROOT / "content/entities").glob("*.jsonld"))]
    resolved, _ = resolve_source_types(classification, documents)

    promotable: list[dict] = []
    below_bar: list[dict] = []
    catalog_total = editorial_total = 0
    reference_only = 0
    missing_level: list[str] = []

    for document in sorted(published_entities(), key=lambda item: item["id"]):
        level = (document.get("metadata") or {}).get("editorial_level")
        if level not in {"catalog", "editorial"}:
            missing_level.append(document["id"])
            continue
        record = evaluate(document, resolved, dependent)
        if record["clearsBar"] and record["independentOnlyByReference"]:
            reference_only += 1
        if level == "catalog":
            catalog_total += 1
            if record["clearsBar"]:
                promotable.append(record)
        else:
            editorial_total += 1
            if not record["clearsBar"]:
                below_bar.append(record)

    baseline = load(BASELINE) if BASELINE.is_file() else {"maximums": {}, "minimums": {}}
    ceiling = baseline.get("maximums", {}).get("editorialBelowBar")
    errors = [f"{entity_id}: entity has no editorial_level" for entity_id in missing_level]

    # Ratchet: an entity may not be marked editorial below the bar unless it was
    # already there when the bar was declared. The debt shrinks, never grows.
    if ceiling is not None and len(below_bar) > ceiling:
        errors.append(
            f"editorial entities below the promotion bar grew: {len(below_bar)} now, baseline allows {ceiling}"
        )

    report = {
        "version": "1.0.0",
        "status": "PASS" if not errors else "FAIL",
        "bar": {
            "evidencedClaims": 1,
            "independentSources": 1,
            "note": "Promoção exige ao menos um claim com evidência e ao menos uma fonte fora da parte interessada.",
        },
        "summary": {
            "catalogEntities": catalog_total,
            "editorialEntities": editorial_total,
            "promotableCatalogEntities": len(promotable),
            "editorialBelowBar": len(below_bar),
            "clearingBarOnlyByReference": reference_only,
        },
        "belowBarByType": dict(sorted(Counter(item["type"] for item in below_bar).items())),
        "baseline": {"editorialBelowBarCeiling": ceiling},
        "promotable": promotable,
        "belowBar": below_bar,
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
        baseline.setdefault("maximums", {})["editorialBelowBar"] = report["summary"]["editorialBelowBar"]
        dump(BASELINE, baseline)
        report = audit()

    if args.check:
        if not args.output.is_file() or load(args.output) != report:
            raise SystemExit("catalog promotion report is stale; regenerate it")
    else:
        dump(args.output, report)

    print(json.dumps({"status": report["status"], **report["summary"]}, ensure_ascii=False, sort_keys=True))
    if report["status"] != "PASS":
        raise SystemExit("\n".join(report["errors"]))


if __name__ == "__main__":
    main()
