"""Validate spatial classification and temporal geometry coverage."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "content" / "spatial-inventory.json"
REPORT = ROOT / "reports" / "spatial-coverage.json"
MODES = {"interactive-required", "static-sufficient", "not-spatial"}
PRECISIONS = {"entrance", "centroid", "site", "route", "boundary", "approximate", "city", "locality", "facility", "facility-approximate"}
CONFIDENCES = {"verified", "probable", "approximate", "high"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def audit() -> dict:
    inventory = load(INVENTORY)
    chapters = load(ROOT / "content" / "annual-chapters.json")["chapters"]
    expected = {(item["year"], item["entity"]) for item in chapters}
    actual = {(item.get("year"), item.get("entity")) for item in inventory.get("items", [])}
    errors: list[str] = []
    if expected != actual or len(actual) != 258:
        errors.append("inventory must classify each annual chapter exactly once")

    geometry_by_entity: dict[str, list[dict]] = {}
    features = 0
    for path in sorted((ROOT / "content" / "geography").glob("*.geojson")):
        for feature in load(path).get("features", []):
            features += 1
            props = feature.get("properties", {})
            entity = props.get("entity", "")
            geometry_by_entity.setdefault(entity, []).append(feature)
            validity = props.get("validity", {})
            if not validity.get("from") or not validity.get("until") or not validity.get("precision"):
                errors.append(f"{feature.get('id')}: incomplete temporal validity")
            if props.get("precision") not in PRECISIONS:
                errors.append(f"{feature.get('id')}: invalid precision")
            if props.get("confidence") not in CONFIDENCES:
                errors.append(f"{feature.get('id')}: invalid confidence")
            if not props.get("source"):
                errors.append(f"{feature.get('id')}: missing source")

    items = inventory.get("items", [])
    for item in items:
        if item.get("mode") not in MODES or len(item.get("rationale", "")) < 20:
            errors.append(f"{item.get('year')}: invalid spatial classification")
        has_geometry = bool(geometry_by_entity.get(item.get("geometryEntity", item.get("entity", ""))))
        expected_status = "covered" if has_geometry else ("pending" if item.get("mode") == "interactive-required" else "not-required")
        if item.get("geometryStatus") != expected_status:
            errors.append(f"{item.get('year')}: stale geometry status")

    required = [item for item in items if item.get("mode") == "interactive-required"]
    covered = [item for item in required if item.get("geometryStatus") == "covered"]
    summary = {
        "chapters": len(items),
        "interactiveRequired": len(required),
        "staticSufficient": sum(item.get("mode") == "static-sufficient" for item in items),
        "notSpatial": sum(item.get("mode") == "not-spatial" for item in items),
        "interactiveCovered": len(covered),
        "interactivePending": len(required) - len(covered),
        "geographyFeatures": features,
    }
    report = {"version": "1.0.0", "status": "PASS" if not errors else "FAIL", "summary": summary, "errors": errors}
    canonical = json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    report["reportSha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    report = audit()
    if args.check:
        if not REPORT.is_file() or load(REPORT) != report:
            raise SystemExit("spatial coverage report is stale; regenerate it")
    else:
        REPORT.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], **report["summary"], "reportSha256": report["reportSha256"]}, ensure_ascii=False, sort_keys=True))
    if report["status"] != "PASS":
        raise SystemExit("\n".join(report["errors"]))


if __name__ == "__main__":
    main()
