"""Audit whether editorial claims are confrontable by a source outside the interested party.

The Atlas accepts manufacturer communication as evidence; it does not accept it as
the *only* evidence for an editorial entity. This audit does not judge whether a
fact is true — it judges whether the record allows someone to check it against a
party that did not build the car.

The gate is a ratchet, not a wall. Publishing v2.0.0 left a declared debt of
entities sustained only by the interested party; that debt may shrink and may not
grow. New editorial work therefore has to clear the bar, while the existing
corpus is remediated in batches instead of failing the build on day one.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLASSIFICATION = ROOT / "content/source-classification.json"
REGISTRY = ROOT / "migration/sources.jsonld"
BASELINE = ROOT / "gates/editorial-baseline.json"
DEFAULT_REPORT = ROOT / "reports" / "source-independence.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def all_documents() -> list[dict]:
    """Every entity file on disk, including documents the build discards."""
    paths = sorted((ROOT / "migration/entities").glob("*.jsonld"))
    paths += sorted((ROOT / "content/entities").glob("*.jsonld"))
    return [load(path) for path in paths]


def published_entities() -> list[dict]:
    """The entity set the bundles actually publish.

    Five identities exist in both corpora. content/entities is the authority and
    wins, matching build_bundles.py and audit_c18_semantics.py: a gate has to
    measure what ships, not what sits on disk.
    """
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


def source_index(documents: list[dict], classification: dict) -> tuple[dict[str, str], list[str]]:
    """Resolve every source to a sourceType.

    The migration registry declares the field; the 103 sources written inline in
    content/entities/ do not, so they are classified by publisher through the
    versioned map. A source that resolves to neither is an error: the gate must
    not silently treat an unclassified source as independent.
    """
    publishers = classification["publisherSourceTypes"]
    resolved: dict[str, str] = {
        item["id"]: item["sourceType"]
        for item in load(REGISTRY)["items"]
        if item.get("sourceType")
    }
    unclassified: list[str] = []
    for document in documents:
        for source in document.get("sources") or []:
            if not isinstance(source, dict) or source["id"] in resolved:
                continue
            source_type = source.get("sourceType") or publishers.get(source.get("publisher", ""))
            if source_type:
                resolved[source["id"]] = source_type
            else:
                unclassified.append(f'{source["id"]}: publisher {source.get("publisher") or "(ausente)"}')
    return resolved, sorted(set(unclassified))



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
    # Sources are resolved from every file so that an unclassified source is
    # caught even in a document the build discards; the audit itself only judges
    # what is published.
    resolved, unclassified = source_index(all_documents(), classification)
    documents = published_entities()

    errors = list(unclassified)
    independent_entities: list[str] = []
    dependent_only: list[str] = []
    unresolved_citations: list[str] = []
    citation_types: Counter[str] = Counter()

    for document in documents:
        claims = document.get("claims") or []
        if not claims or (document.get("metadata") or {}).get("editorial_level") != "editorial":
            continue
        types: list[str] = []
        for claim in claims:
            for source_id in claim.get("sources") or []:
                source_type = resolved.get(source_id)
                if source_type is None:
                    unresolved_citations.append(f'{document["id"]}: unclassified source {source_id}')
                    continue
                types.append(source_type)
                citation_types[source_type] += 1
        if any(source_type not in dependent for source_type in types):
            independent_entities.append(document["id"])
        else:
            dependent_only.append(document["id"])

    errors.extend(sorted(set(unresolved_citations)))
    audited = len(independent_entities) + len(dependent_only)
    baseline = load(BASELINE) if BASELINE.is_file() else {"maximums": {}, "minimums": {}}
    ceiling = baseline.get("maximums", {}).get("dependentOnlyEntities")
    floor = baseline.get("minimums", {}).get("independentEntities")

    # Ratchet: the declared debt may shrink, never grow, and the confrontable
    # core may grow, never shrink. Expanding the acervo is always allowed; doing
    # it below the bar is not.
    if ceiling is not None and len(dependent_only) > ceiling:
        errors.append(
            f"declared debt grew: {len(dependent_only)} entities sustained only by the interested party, "
            f"baseline allows {ceiling}"
        )
    if floor is not None and len(independent_entities) < floor:
        errors.append(
            f"confrontable core shrank: {len(independent_entities)} entities, baseline requires {floor}"
        )

    report = {
        "version": "1.0.0",
        "status": "PASS" if not errors else "FAIL",
        "summary": {
            "editorialEntitiesWithClaims": audited,
            "independentEntities": len(independent_entities),
            "dependentOnlyEntities": len(dependent_only),
            "sourcesClassified": len(resolved),
            "sourcesUnclassified": len(unclassified),
            "citations": sum(citation_types.values()),
            "dependentCitations": sum(count for kind, count in citation_types.items() if kind in dependent),
        },
        "citationsBySourceType": dict(sorted(citation_types.items())),
        "baseline": {"dependentOnlyCeiling": ceiling, "independentFloor": floor},
        "debt": sorted(dependent_only),
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
        baseline.setdefault("maximums", {})["dependentOnlyEntities"] = report["summary"]["dependentOnlyEntities"]
        baseline.setdefault("minimums", {})["independentEntities"] = report["summary"]["independentEntities"]
        dump(BASELINE, baseline)
        report = audit()

    if args.check:
        if not args.output.is_file() or load(args.output) != report:
            raise SystemExit("source independence report is stale; regenerate it")
    else:
        dump(args.output, report)

    print(json.dumps({"status": report["status"], **report["summary"]}, ensure_ascii=False, sort_keys=True))
    if report["status"] != "PASS":
        raise SystemExit("\n".join(report["errors"]))


if __name__ == "__main__":
    main()
