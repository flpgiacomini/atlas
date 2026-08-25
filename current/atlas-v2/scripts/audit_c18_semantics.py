"""Close C18 with a deterministic, transversal semantic audit of CP19.

The audit deliberately separates catalog eligibility from narrative readiness.
An individually matched automotive identity may enter discovery without gaining
unsupported dates, genealogy or historical claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT.parent / "atlas-web"
REVIEWS = ROOT / "content/canonical-curation-reviews.json"
DECISIONS = ROOT / "content/canonical-curation-decisions.json"
SOURCES = ROOT / "migration/sources.jsonld"
RESEARCH = WEB / "data/imports/atlas-curation/brands-c07-c17.research.json"
OUTPUT = ROOT / "content/c18-semantic-audit.json"
REPORT = ROOT / "reports/c18-semantic-audit.json"

INTERNAL_RETENTION_SOURCE = "atlas:source:projeto-atlas-c07-c17-unresolved-identity-audit"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold())
    return re.sub(r"[^a-z0-9]+", "", "".join(ch for ch in value if not unicodedata.combining(ch)))


def entity_documents() -> list[dict]:
    paths = sorted((ROOT / "migration/entities").glob("*.jsonld"))
    paths += sorted((ROOT / "content/entities").glob("*.jsonld"))
    return [load(path) for path in paths]


def build() -> tuple[dict, dict]:
    reviews = load(REVIEWS)["reviews"]
    decisions = load(DECISIONS)["queue"]
    sources = {item["id"]: item for item in load(SOURCES)["items"]}
    entities = {item["id"]: item for item in entity_documents()}
    research = {item["candidateName"]: item for item in load(RESEARCH)["records"]}
    milestones = load(ROOT / "content/brand-timeline.json")["milestones"]
    relations = load(ROOT / "content/brand-relations.json")["relations"]

    reviews_by_id = {item["candidateId"]: item for item in reviews}
    decisions_by_id = {item["canonicalId"]: item for item in decisions}
    milestone_counts = Counter(item["brand"] for item in milestones)
    relation_counts = Counter(value for item in relations for value in (item["from"], item["to"]))
    normalized_names: dict[str, list[str]] = defaultdict(list)
    records: list[dict] = []
    errors: list[str] = []

    if len(reviews) != 522 or len(decisions) != 522:
        errors.append("C18 requires the complete 522-item canonical queue")
    if set(reviews_by_id) != set(decisions_by_id):
        errors.append("review and decision identity sets diverge")

    for candidate_id in sorted(reviews_by_id):
        review = reviews_by_id[candidate_id]
        decision = decisions_by_id[candidate_id]
        entity = entities.get(candidate_id)
        prefix = candidate_id
        item_errors: list[str] = []
        if not entity:
            errors.append(f"{prefix}: missing canonical entity")
            continue
        name = entity.get("name", "").strip()
        normalized_names[normalized(name)].append(candidate_id)
        if not name or entity.get("type") not in {"Brand", "Vehicle"}:
            item_errors.append("invalid canonical identity")
        if not entity.get("legacy", {}).get("id"):
            item_errors.append("legacy identity map missing")
        aliases = entity.get("aliases", [])
        alias_values = [value if isinstance(value, str) else value.get("name", "") for value in aliases]
        alias_norms = [normalized(value) for value in alias_values if value]
        if len(alias_norms) != len(set(alias_norms)) or normalized(name) in alias_norms:
            item_errors.append("duplicate or self alias")

        source_docs = [sources.get(source_id) for source_id in review.get("sourceIds", [])]
        if not source_docs or any(source is None for source in source_docs):
            item_errors.append("unresolved review source")
        for source in filter(None, source_docs):
            parsed = urlparse(source.get("url", ""))
            if parsed.scheme != "https" or not parsed.netloc:
                item_errors.append("non-HTTPS source")
            if source.get("trust") not in {"primary", "institutional", "specialist"}:
                item_errors.append("unaccepted source trust")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", source.get("verifiedAt", "")):
                item_errors.append("source verification date missing")
        assertions = review.get("assertions", [])
        if len(assertions) < 2 or any(not value.get("locator") or not value.get("text") for value in assertions):
            item_errors.append("assertion or locator missing")
        if not review.get("rationale"):
            item_errors.append("decision rationale missing")

        metadata = entity.get("metadata", {})
        if metadata.get("curation_review") != review["id"] or metadata.get("curation_decision") != review["decision"]:
            item_errors.append("entity/review trace mismatch")
        expected_state = "approved_pending_v2_cut" if review["decision"] == "promote-editorial" else "retained_catalog_after_review"
        if metadata.get("promotion_state") != expected_state:
            item_errors.append("promotion-state mismatch")

        research_item = research.get(name)
        source_scope = "individual"
        narrative_scope = "claim-backed"
        identity_resolution = "canonical-and-source-matched"
        if entity["type"] == "Brand" and metadata.get("curation_batch", "").split("-")[0] in {f"C{i:02d}" for i in range(7, 18)}:
            if not research_item:
                item_errors.append("C07-C17 research trace missing")
            elif review["decision"] == "promote-editorial":
                # The research collector tests the page introduction *and* its
                # categories before compacting the snapshot. The introduction
                # itself is intentionally not redistributed; validate the
                # immutable acceptance trace instead of attempting to recreate
                # that test from the compact category subset.
                required_trace = ("title", "url", "pageId", "revisionId", "revisionTimestamp", "verifiedAt")
                compact_match = research_item.get("status") == "matched" and not any(
                    not research_item.get(key) for key in required_trace
                )
                manual_wikidata = (
                    metadata.get("research_match_method") == "manual-wikidata"
                    and all(source and source.get("publisher") == "Wikidata contributors" for source in source_docs)
                    and all(source.get("externalIds", {}).get("wikidata") for source in source_docs if source)
                )
                if not compact_match and not manual_wikidata:
                    item_errors.append("promoted brand lacks immutable automotive match trace")
                if INTERNAL_RETENTION_SOURCE in review["sourceIds"]:
                    item_errors.append("promotion cannot use unresolved-identity source")
                narrative_scope = "identity-only"
            else:
                if research_item.get("status") != "unresolved":
                    item_errors.append("retention/research status mismatch")
                if review["sourceIds"] != [INTERNAL_RETENTION_SOURCE]:
                    item_errors.append("unresolved retention trace mismatch")
                source_scope = "negative-search-audit"
                narrative_scope = "catalog-only-no-public-claims"
                identity_resolution = "legacy-identity-preserved-contribution-unproven"
                safeguard = (entity.get("description", "") + " " + review["rationale"]).casefold()
                if "nenhuma" not in safeguard and "não" not in safeguard:
                    item_errors.append("retention lacks non-publication safeguard")

        claims = entity.get("claims", [])
        for claim in claims:
            if not claim.get("sources") or not claim.get("evidence"):
                item_errors.append("claim lacks source or evidence")
            if any(ref not in sources for ref in claim.get("sources", [])):
                item_errors.append("claim source unresolved")
        if narrative_scope == "claim-backed" and review["decision"] == "promote-editorial" and not claims:
            # Early brand reviews can be source-backed without legacy Claim objects;
            # their permitted publication remains limited to the reviewed assertions.
            narrative_scope = "assertion-backed"

        chronology = "documented" if milestone_counts[candidate_id] else "not-asserted"
        genealogy = "documented" if relation_counts[candidate_id] else "not-asserted"
        records.append({
            "candidateId": candidate_id,
            "name": name,
            "entityType": entity["type"],
            "decision": review["decision"],
            "identity": {
                "status": identity_resolution,
                "legacyId": entity["legacy"]["id"],
                "aliases": alias_values,
                "matchedTitle": research_item.get("title") if research_item else None,
                "externalId": research_item.get("wikidataId") if research_item else None,
            },
            "evidence": {
                "sourceScope": source_scope,
                "sourceIds": review["sourceIds"],
                "assertionCount": len(assertions),
                "claimCount": len(claims),
                "narrativeScope": narrative_scope,
            },
            "temporal": {"status": chronology, "milestoneCount": milestone_counts[candidate_id]},
            "genealogy": {"status": genealogy, "relationCount": relation_counts[candidate_id]},
            "regional": {
                "status": "classified" if entity["type"] == "Brand" else "not-applicable",
                "region": metadata.get("region_cluster"),
                "wave": metadata.get("wave"),
            },
            "scope": {
                "catalogEligibility": "approved" if review["decision"] == "promote-editorial" else "retained",
                "publicNarrativeAllowed": narrative_scope not in {"identity-only", "catalog-only-no-public-claims"},
            },
            "status": "PASS" if not item_errors else "FAIL",
            "errors": item_errors,
        })
        errors.extend(f"{prefix}: {error}" for error in item_errors)

    collisions = {key: values for key, values in normalized_names.items() if key and len(values) > 1}
    if collisions:
        errors.extend(f"normalized identity collision: {values}" for values in collisions.values())

    decision_counts = Counter(item["decision"] for item in records)
    scope_counts = Counter(item["evidence"]["narrativeScope"] for item in records)
    region_counts = Counter(item["regional"]["region"] for item in records if item["regional"]["region"])
    audit = {
        "version": "2.0.0",
        "checkpoint": "C18",
        "policy": {
            "promotion": "Aprova elegibilidade editorial, mas a narrativa pública permanece limitada ao escopo de evidência registrado.",
            "identityOnly": "Permite descoberta e identificação; proíbe datas, contribuições e genealogia sem claim ou assertion próprio.",
            "retention": "Preserva a identidade no catálogo e proíbe alegações públicas novas até evidência individual inequívoca.",
            "absence": "A ausência de marco ou relação significa não afirmado, nunca inexistente.",
        },
        "records": records,
    }
    audit_text = canonical(audit)
    report = {
        "status": "PASS" if not errors else "FAIL",
        "checkpoint": "C18",
        "audited": len(records),
        "passed": sum(item["status"] == "PASS" for item in records),
        "failed": sum(item["status"] == "FAIL" for item in records),
        "decisions": dict(sorted(decision_counts.items())),
        "narrativeScopes": dict(sorted(scope_counts.items())),
        "identityCollisions": len(collisions),
        "regions": dict(sorted(region_counts.items())),
        "timeline": {"brands": len(milestone_counts), "milestones": len(milestones)},
        "genealogy": {"participants": len(relation_counts), "relations": len(relations)},
        "contributionUnprovenRetentions": sum(
            item["identity"]["status"] == "legacy-identity-preserved-contribution-unproven" for item in records
        ),
        "auditSha256": hashlib.sha256(audit_text.encode()).hexdigest(),
        "errors": errors,
    }
    return audit, report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    audit, report = build()
    expected_audit, expected_report = canonical(audit), canonical(report)
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected_audit:
            raise SystemExit("C18 semantic audit is stale")
        if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != expected_report:
            raise SystemExit("C18 semantic report is stale")
    else:
        OUTPUT.write_text(expected_audit, encoding="utf-8")
        REPORT.write_text(expected_report, encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
