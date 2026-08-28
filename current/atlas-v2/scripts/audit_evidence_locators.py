"""Audit whether the evidence chain actually leads anywhere.

Every claim in the Atlas carries evidence and a source; none is orphaned, and the
contract validators already guarantee that. This audit asks the question those
validators cannot: given the source, can a reader find the assertion inside it?

Three locator grades answer that. A *documentary* locator names a recoverable
position — a section, a page, a quote, an inventory number. A *deferred* locator
announces its own absence, and the corpus carries hundreds left behind by the
import batches ("refine page/section locator during deep curation"). A *nominal*
locator restates the claim's own subject and predicate, which tells a reader what
was asserted but never where it was read.

The gate is the same ratchet used for source independence: the documentary core
may grow and not shrink, the debt may shrink and not grow.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "content/evidence-policy.json"
EVIDENCE = ROOT / "migration/evidence.jsonld"
BASELINE = ROOT / "gates/editorial-baseline.json"
DEFAULT_REPORT = ROOT / "reports" / "evidence-locators.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def merge_entity(migrated: dict, authored: dict) -> dict:
    """Union two documents describing the same identity; see build_bundles.py."""
    merged = {**migrated, **authored}
    authored_claims = authored.get("claims") or []
    known = {claim["id"] for claim in authored_claims}
    inherited = [claim for claim in migrated.get("claims") or [] if claim["id"] not in known]
    merged["claims"] = sorted(authored_claims + inherited, key=lambda claim: claim["id"])
    return merged


def published_entities() -> list[dict]:
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


def evidence_index() -> dict[str, dict]:
    index = {item["id"]: item for item in load(EVIDENCE)["items"]}
    for path in sorted((ROOT / "content/entities").glob("*.jsonld")):
        for item in load(path).get("evidence") or []:
            index[item["id"]] = item
    return index


def grade(item: dict, documentary_keys: set[str], deferred: re.Pattern[str], excerpt_counts: bool) -> str:
    locator = item.get("locator") or {}
    # A verbatim excerpt locates the assertion more strongly than any key can.
    if excerpt_counts and str(item.get("excerpt") or "").strip():
        return "documentary"
    if set(locator) & documentary_keys:
        return "documentary"
    if any(deferred.search(str(value)) for value in locator.values() if isinstance(value, str)):
        return "deferred"
    return "nominal"


def audit() -> dict:
    policy = load(POLICY)
    documentary_keys = set(policy["documentaryLocatorKeys"])
    deferred = re.compile(policy["deferredLocatorPattern"], re.IGNORECASE)
    evidence = evidence_index()
    excerpt_counts = bool(policy.get("excerptIsDocumentary"))
    grades = {item_id: grade(item, documentary_keys, deferred, excerpt_counts) for item_id, item in evidence.items()}

    documented: list[str] = []
    queue: list[dict] = []
    unresolved: list[str] = []

    for document in sorted(published_entities(), key=lambda item: item["id"]):
        claims = document.get("claims") or []
        if not claims or (document.get("metadata") or {}).get("editorial_level") != "editorial":
            continue
        counts: Counter[str] = Counter()
        for claim in claims:
            for evidence_id in claim.get("evidence") or []:
                if evidence_id not in grades:
                    unresolved.append(f'{document["id"]}: unresolved evidence {evidence_id}')
                    continue
                counts[grades[evidence_id]] += 1
        if counts["documentary"]:
            documented.append(document["id"])
        else:
            queue.append({
                "id": document["id"],
                "name": document.get("name"),
                "type": document.get("type"),
                "claimCount": len(claims),
                # The queue is a worklist, so it ranks by what an entity asserts,
                # not by how many sources were attached to those assertions.
                "statementCount": len({claim.get("statementLegacyId") or claim["id"] for claim in claims}),
                "deferredLocators": counts["deferred"],
                "nominalLocators": counts["nominal"],
            })

    audited = len(documented) + len(queue)
    baseline = load(BASELINE) if BASELINE.is_file() else {"maximums": {}, "minimums": {}}
    ceiling = baseline.get("maximums", {}).get("entitiesWithoutDocumentaryEvidence")
    floor = baseline.get("minimums", {}).get("entitiesWithDocumentaryEvidence")
    errors = sorted(set(unresolved))

    if ceiling is not None and len(queue) > ceiling:
        errors.append(
            f"entities without documentary evidence grew: {len(queue)} now, baseline allows {ceiling}"
        )
    if floor is not None and len(documented) < floor:
        errors.append(
            f"documented core shrank: {len(documented)} entities, baseline requires {floor}"
        )

    report = {
        "version": "1.0.0",
        "status": "PASS" if not errors else "FAIL",
        "summary": {
            "evidenceRecords": len(evidence),
            "documentaryEvidence": sum(value == "documentary" for value in grades.values()),
            "deferredEvidence": sum(value == "deferred" for value in grades.values()),
            "nominalEvidence": sum(value == "nominal" for value in grades.values()),
            "editorialEntitiesWithClaims": audited,
            "entitiesWithDocumentaryEvidence": len(documented),
            "entitiesWithoutDocumentaryEvidence": len(queue),
        },
        "queueByType": dict(sorted(Counter(item["type"] for item in queue).items())),
        "baseline": {"withoutDocumentaryCeiling": ceiling, "documentedFloor": floor},
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
        baseline.setdefault("maximums", {})["entitiesWithoutDocumentaryEvidence"] = report["summary"]["entitiesWithoutDocumentaryEvidence"]
        baseline.setdefault("minimums", {})["entitiesWithDocumentaryEvidence"] = report["summary"]["entitiesWithDocumentaryEvidence"]
        dump(BASELINE, baseline)
        report = audit()

    if args.check:
        if not args.output.is_file() or load(args.output) != report:
            raise SystemExit("evidence locator report is stale; regenerate it")
    else:
        dump(args.output, report)

    print(json.dumps({"status": report["status"], **report["summary"]}, ensure_ascii=False, sort_keys=True))
    if report["status"] != "PASS":
        raise SystemExit("\n".join(report["errors"]))


if __name__ == "__main__":
    main()
