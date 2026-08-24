"""Validate exact-year editorial chapters and their canonical entity links."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate() -> dict:
    doc = load(ROOT / "content/annual-chapters.json")
    entities = [load(path) for path in (ROOT / "migration/entities").glob("*.jsonld")]
    entities += [load(path) for path in (ROOT / "content/entities").glob("*.jsonld")]
    entity_ids = {item["id"] for item in entities}
    years: set[int] = set()
    copies: set[str] = set()
    errors: list[str] = []
    for chapter in doc.get("chapters", []):
        year = chapter.get("year")
        if not isinstance(year, int) or not 1769 <= year <= 2026:
            errors.append(f"invalid year: {year!r}")
        if year in years:
            errors.append(f"duplicate year: {year}")
        years.add(year)
        kind = chapter.get("chapterKind", "milestone")
        if kind not in {"milestone", "continuity"}:
            errors.append(f"{year}: invalid chapterKind {kind!r}")
        if chapter.get("entity") not in entity_ids:
            errors.append(f"{year}: unresolved entity {chapter.get('entity')}")
        for field in ("label", "eyebrow", "title", "copy", "place", "asset"):
            if not isinstance(chapter.get(field), str) or not chapter[field].strip():
                errors.append(f"{year}: missing {field}")
        copy = chapter.get("copy", "").strip()
        if copy in copies:
            errors.append(f"{year}: duplicated narrative")
        copies.add(copy)
    missing_first_span = set(range(1769, 1940)) - years
    if missing_first_span:
        errors.append(f"missing years in continuous precursor span: {sorted(missing_first_span)}")
    if errors:
        raise SystemExit("\n".join(errors))
    return {"status": "PASS", "chapters": len(years), "from": min(years), "until": max(years)}


if __name__ == "__main__":
    print(json.dumps(validate(), sort_keys=True))
