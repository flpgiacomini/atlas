"""Audit the six required editorial journeys across story, evidence, media and geography."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT.parent / "atlas-v2-prototype" / "public"
DEFAULT_REPORT = ROOT / "reports" / "journey-coverage.json"
REQUIRED_MEDIA = {
    "id", "journeyEntity", "file", "mediaType", "author", "originalSource",
    "license", "licenseUrl", "credit", "alt", "verifiedAt", "nature",
    "historicalDocument",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def story_years() -> set[int]:
    years: set[int] = set()
    for path in (ROOT / "content" / "stories").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        match = re.search(r"^year:\s*(\d{4})\s*$", text, re.MULTILINE)
        complete = re.search(r"^status:\s*complete\s*$", text, re.MULTILINE)
        if match and complete:
            years.add(int(match.group(1)))
    return years


def audit() -> dict:
    journeys = load(ROOT / "content" / "journeys.json")["journeys"]
    entities: dict[str, dict] = {}
    for directory in (ROOT / "migration" / "entities", ROOT / "content" / "entities"):
        for path in directory.glob("*.jsonld"):
            entity = load(path)
            entities[entity["id"]] = entity

    mapped_entities: set[str] = set()
    for path in (ROOT / "content" / "geography").glob("*.geojson"):
        for feature in load(path).get("features", []):
            if entity_id := feature.get("properties", {}).get("entity"):
                mapped_entities.add(entity_id)

    media_items = load(ROOT / "content" / "media-manifest.json")["items"]
    media_by_entity: dict[str, list[dict]] = {}
    errors: list[str] = []
    for item in media_items:
        missing = REQUIRED_MEDIA - set(item)
        if missing:
            errors.append(f"{item.get('id', 'media')}: missing fields {sorted(missing)}")
        if not (ASSET_ROOT / str(item.get("file", "")).lstrip("/")).is_file():
            errors.append(f"{item.get('id', 'media')}: missing local file")
        parsed = urlparse(item.get("licenseUrl", ""))
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"{item.get('id', 'media')}: invalid license URL")
        if len(item.get("alt", "").strip()) < 20 or len(item.get("credit", "").strip()) < 10:
            errors.append(f"{item.get('id', 'media')}: incomplete accessibility or credit")
        media_by_entity.setdefault(item.get("journeyEntity", ""), []).append(item)

    authored_years = story_years()
    items: list[dict] = []
    for journey in journeys:
        entity = entities.get(journey["entity"])
        claims = (entity or {}).get("claims", [])
        source_ids = {source for claim in claims for source in claim.get("sources", [])}
        evidence_ids = {evidence for claim in claims for evidence in claim.get("evidence", [])}
        item = {
            "entity": journey["entity"],
            "label": journey["label"],
            "year": journey["year"],
            "canonicalEvidence": bool(entity and claims and source_ids and evidence_ids),
            "authoredStory": journey["year"] in authored_years,
            "licensedMedia": len(media_by_entity.get(journey["entity"], [])),
            "temporalGeography": journey["entity"] in mapped_entities,
            "presentationAsset": (ASSET_ROOT / journey["asset"].lstrip("/")).is_file(),
        }
        item["complete"] = all((item["canonicalEvidence"], item["authoredStory"], item["licensedMedia"], item["temporalGeography"], item["presentationAsset"]))
        items.append(item)

    if len(journeys) != 6:
        errors.append(f"expected six journeys, found {len(journeys)}")
    report = {
        "version": "1.0.0",
        "status": "PASS" if not errors else "FAIL",
        "summary": {
            "journeys": len(items),
            "canonicalEvidence": sum(item["canonicalEvidence"] for item in items),
            "authoredStories": sum(item["authoredStory"] for item in items),
            "journeysWithLicensedMedia": sum(bool(item["licensedMedia"]) for item in items),
            "journeysWithTemporalGeography": sum(item["temporalGeography"] for item in items),
            "presentationAssets": sum(item["presentationAsset"] for item in items),
            "completeJourneys": sum(item["complete"] for item in items),
        },
        "items": items,
        "errors": errors,
    }
    canonical = json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    report["reportSha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    report = audit()
    if args.check:
        if not args.output.is_file() or load(args.output) != report:
            raise SystemExit("journey coverage report is stale; regenerate it")
    else:
        dump(args.output, report)
    print(json.dumps({"status": report["status"], **report["summary"], "reportSha256": report["reportSha256"]}, ensure_ascii=False, sort_keys=True))
    if report["status"] != "PASS":
        raise SystemExit("\n".join(report["errors"]))


if __name__ == "__main__":
    main()
