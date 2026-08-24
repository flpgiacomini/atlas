"""Audit narrative, temporal, source, media and geography coverage for annual chapters."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
APP_PUBLIC = ROOT.parent / "atlas-v2-app" / "public"
DEFAULT_REPORT = ROOT / "reports" / "editorial-coverage.json"


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


def claim_years(claim: dict) -> tuple[set[int], tuple[int, int] | None]:
    points: set[int] = set()
    obj = claim.get("object")
    if isinstance(obj, dict) and obj.get("type") == "date":
        if parsed := year(obj.get("value")):
            points.add(parsed)
    validity = claim.get("validity", {})
    start, end = year(validity.get("from")), year(validity.get("until"))
    points.update(value for value in (start, end) if value is not None)
    return points, (start, end) if start is not None and end is not None else None


def audit() -> dict:
    chapters = load(ROOT / "content" / "annual-chapters.json")["chapters"]
    entities: dict[str, dict] = {}
    for directory in (ROOT / "migration" / "entities", ROOT / "content" / "entities"):
        for path in sorted(directory.glob("*.jsonld")):
            document = load(path)
            entities[document["id"]] = document

    migrated_sources = load(ROOT / "migration" / "sources.jsonld")["items"]
    migrated_evidence = load(ROOT / "migration" / "evidence.jsonld")["items"]
    sources = {item["id"]: item for item in migrated_sources}
    evidence = {item["id"]: item for item in migrated_evidence}
    for entity in entities.values():
        sources.update({item["id"]: item for item in entity.get("sources", [])})
        evidence.update({item["id"]: item for item in entity.get("evidence", [])})

    geometry_entities: set[str] = set()
    geometry_features = 0
    for path in sorted((ROOT / "content" / "geography").glob("*.geojson")):
        for feature in load(path).get("features", []):
            geometry_features += 1
            if entity_id := feature.get("properties", {}).get("entity"):
                geometry_entities.add(entity_id)

    errors: list[str] = []
    exact_years: list[int] = []
    interval_years: list[int] = []
    temporal_gaps: list[dict] = []
    mapped_years: list[int] = []
    asset_usage: Counter[str] = Counter()
    asset_missing: list[dict] = []
    chapter_source_counts: list[int] = []

    for chapter in chapters:
        chapter_year = chapter["year"]
        entity = entities.get(chapter.get("entity"))
        if entity is None:
            errors.append(f"{chapter_year}: unresolved entity {chapter.get('entity')}")
            continue
        claims = entity.get("claims", [])
        source_ids = {ref for claim in claims for ref in claim.get("sources", [])}
        evidence_ids = {ref for claim in claims for ref in claim.get("evidence", [])}
        chapter_source_counts.append(len(source_ids))
        if not claims or not source_ids or not evidence_ids:
            errors.append(f"{chapter_year}: entity lacks claims, sources or evidence")
        for source_id in source_ids:
            source = sources.get(source_id)
            if source is None:
                errors.append(f"{chapter_year}: unresolved source {source_id}")
                continue
            parsed = urlparse(source.get("url", ""))
            if parsed.scheme != "https" or not parsed.netloc:
                errors.append(f"{chapter_year}: invalid source URL {source_id}")
        for evidence_id in evidence_ids:
            item = evidence.get(evidence_id)
            if item is None:
                errors.append(f"{chapter_year}: unresolved evidence {evidence_id}")
            elif item.get("source") not in sources:
                errors.append(f"{chapter_year}: evidence has unresolved source {evidence_id}")

        exact = False
        interval = False
        for claim in claims:
            points, span = claim_years(claim)
            exact = exact or chapter_year in points
            interval = interval or bool(span and span[0] <= chapter_year <= span[1])
        if exact:
            exact_years.append(chapter_year)
        if exact or interval:
            interval_years.append(chapter_year)
        else:
            temporal_gaps.append({"year": chapter_year, "entity": entity["id"]})

        if entity["id"] in geometry_entities:
            mapped_years.append(chapter_year)
        asset = chapter.get("asset", "")
        asset_usage[asset] += 1
        asset_path = APP_PUBLIC / asset.lstrip("/")
        if not asset or not asset_path.is_file():
            asset_missing.append({"year": chapter_year, "asset": asset})

        for field, minimum in (("title", 20), ("copy", 100)):
            if len(chapter.get(field, "").strip()) < minimum:
                errors.append(f"{chapter_year}: {field} below editorial minimum")

    if len(chapters) != 258 or {item["year"] for item in chapters} != set(range(1769, 2027)):
        errors.append("annual publication must contain exactly 258 chapters from 1769 to 2026")
    if asset_missing:
        errors.append(f"{len(asset_missing)} chapter assets are missing")

    manifest_candidates = [
        ROOT / "content" / "media-manifest.json",
        ROOT / "content" / "media-manifest.jsonld",
    ]
    media_manifest = next((path for path in manifest_candidates if path.is_file()), None)
    report = {
        "version": "1.0.0",
        "status": "PASS" if not errors else "FAIL",
        "summary": {
            "chapters": len(chapters),
            "entitiesReferenced": len({item["entity"] for item in chapters}),
            "chaptersWithExactYearClaim": len(exact_years),
            "chaptersWithTemporalSupport": len(interval_years),
            "chaptersWithoutTemporalSupport": len(temporal_gaps),
            "chaptersWithMappedEntity": len(mapped_years),
            "geographyFeatures": geometry_features,
            "uniquePresentationAssets": len(asset_usage),
            "chaptersWithExistingAsset": len(chapters) - len(asset_missing),
            "licensedStoryMediaManifest": media_manifest is not None,
            "minimumSourcesPerChapter": min(chapter_source_counts, default=0),
        },
        "coverage": {
            "exactYearClaimYears": exact_years,
            "temporalGapYears": temporal_gaps,
            "mappedYears": mapped_years,
            "assetUsage": dict(sorted(asset_usage.items())),
            "missingAssets": asset_missing,
        },
        "backlog": {
            "temporalClaims": len(temporal_gaps),
            "storyMediaManifest": 0 if media_manifest else 258,
            "spatialStoriesPendingInventory": len(chapters) - len(mapped_years),
            "note": "Spatial backlog is an upper bound until chapters are classified as spatial or non-spatial.",
        },
        "errors": errors,
    }
    canonical = json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    report["reportSha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--check", action="store_true", help="Compare generated report with the versioned report")
    args = parser.parse_args()
    report = audit()
    if args.check:
        if not args.output.is_file() or load(args.output) != report:
            raise SystemExit("editorial coverage report is stale; regenerate it")
    else:
        dump(args.output, report)
    print(json.dumps({"status": report["status"], **report["summary"], "reportSha256": report["reportSha256"]}, ensure_ascii=False, sort_keys=True))
    if report["status"] != "PASS":
        raise SystemExit("\n".join(report["errors"]))


if __name__ == "__main__":
    main()
