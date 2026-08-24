"""Validate CP18 media rights, local files and per-story editorial decisions."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT.parent / "atlas-v2-prototype" / "public"
DEFAULT_REPORT = ROOT / "reports" / "story-media-coverage.json"
REQUIRED_MEDIA = {"id", "journeyEntity", "file", "mediaType", "author", "originalSource", "license", "licenseUrl", "credit", "alt", "verifiedAt", "nature", "historicalDocument"}
ALLOWED_LICENSES = {"CC0 1.0", "CC BY 4.0", "CC BY-SA 4.0", "Public Domain"}
MEDIA_MODES = {"licensed-media", "historical-media", "original-illustration", "editorial-map", "text-led"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def audit() -> dict:
    chapters = load(ROOT / "content" / "annual-chapters.json")["chapters"]
    manifest = load(ROOT / "content" / "media-manifest.json")
    decision_doc = load(ROOT / "content" / "story-media-decisions.json")
    errors: list[str] = []
    media_ids: set[str] = set()

    for item in manifest.get("items", []):
        item_id = item.get("id", "media-without-id")
        missing = REQUIRED_MEDIA - set(item)
        if missing:
            errors.append(f"{item_id}: missing fields {sorted(missing)}")
        if item_id in media_ids:
            errors.append(f"{item_id}: duplicate media id")
        media_ids.add(item_id)
        file_value = item.get("file", "")
        if not file_value.startswith("/assets/") or urlparse(file_value).scheme:
            errors.append(f"{item_id}: media file must be a local /assets path")
        elif not (ASSET_ROOT / file_value.lstrip("/")).is_file():
            errors.append(f"{item_id}: local file is missing")
        if item.get("license") not in ALLOWED_LICENSES:
            errors.append(f"{item_id}: unsupported license {item.get('license')!r}")
        license_url = urlparse(item.get("licenseUrl", ""))
        if license_url.scheme != "https" or not license_url.netloc:
            errors.append(f"{item_id}: invalid license URL")
        if len(item.get("alt", "").strip()) < 30 or len(item.get("credit", "").strip()) < 15:
            errors.append(f"{item_id}: incomplete alt text or credit")
        if item.get("nature") == "historical" and not item.get("historicalDocument"):
            errors.append(f"{item_id}: historical nature must be marked as historical document")

    chapters_by_year = {item["year"]: item for item in chapters}
    decisions = decision_doc.get("decisions", [])
    decisions_by_year: dict[int, dict] = {}
    for decision in decisions:
        decision_year = decision.get("year")
        if decision_year in decisions_by_year:
            errors.append(f"{decision_year}: duplicate story-media decision")
        decisions_by_year[decision_year] = decision
        chapter = chapters_by_year.get(decision_year)
        if not chapter:
            errors.append(f"{decision_year}: decision has no annual chapter")
            continue
        if decision.get("entity") != chapter.get("entity"):
            errors.append(f"{decision_year}: decision entity differs from chapter")
        mode = decision.get("mode")
        refs = decision.get("mediaIds", [])
        if mode not in MEDIA_MODES:
            errors.append(f"{decision_year}: invalid media mode {mode!r}")
        if any(ref not in media_ids for ref in refs):
            errors.append(f"{decision_year}: unresolved media reference")
        if mode == "text-led" and refs:
            errors.append(f"{decision_year}: text-led decision cannot reference media")
        if mode != "text-led" and not refs:
            errors.append(f"{decision_year}: visual decision requires media")
        if len(decision.get("rationale", "").strip()) < 30 or not decision.get("reviewedAt"):
            errors.append(f"{decision_year}: incomplete editorial rationale")

    missing_years = sorted(set(range(1769, 2027)) - set(decisions_by_year))
    if missing_years:
        errors.append(f"missing decisions for {len(missing_years)} chapters")
    if len(decisions) != 258:
        errors.append("story-media registry must contain exactly 258 decisions")

    visual = sorted(item["year"] for item in decisions if item.get("mode") != "text-led")
    text_led = sorted(item["year"] for item in decisions if item.get("mode") == "text-led")
    report = {
        "version": "1.0.0",
        "status": "PASS" if not errors else "FAIL",
        "summary": {
            "chapters": len(chapters),
            "mediaItems": len(media_ids),
            "chaptersWithDecision": len(decisions_by_year),
            "chaptersWithSpecificMedia": len(visual),
            "chaptersTextLed": len(text_led),
            "chaptersWithoutDecision": len(missing_years),
            "externalHotlinks": 0,
        },
        "coverage": {"specificMediaYears": visual, "textLedYears": text_led, "missingDecisionYears": missing_years},
        "backlog": {"specificStoryMedia": len(text_led)},
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
            raise SystemExit("story-media report is stale; regenerate it")
    else:
        dump(args.output, report)
    print(json.dumps({"status": report["status"], **report["summary"], "reportSha256": report["reportSha256"]}, ensure_ascii=False, sort_keys=True))
    if report["status"] != "PASS":
        raise SystemExit("\n".join(report["errors"]))


if __name__ == "__main__":
    main()
