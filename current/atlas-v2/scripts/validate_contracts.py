"""Validate the dependency-free Atlas v2 foundation examples."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"^atlas:[a-z][a-z0-9-]*:[a-z0-9]+(?:-[a-z0-9]+)*$")


def require_semantic_id(value: object, label: str) -> str:
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise ValueError(f"{label}: invalid semantic id {value!r}")
    return value


def canonical_roundtrip(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    encoded = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if json.loads(encoded) != data:
        raise ValueError(f"{path}: non-deterministic JSON round-trip")
    return data


def validate_entity(path: Path) -> set[str]:
    doc = canonical_roundtrip(path)
    require_semantic_id(doc.get("id"), f"{path}:id")
    if doc.get("@context") != "https://flpgiacomini.github.io/atlas/context/v2.jsonld":
        raise ValueError(f"{path}: invalid context")
    sources = {require_semantic_id(source.get("id"), f"{path}:source") for source in doc.get("sources", [])}
    if not sources:
        raise ValueError(f"{path}: entity requires a source")
    for claim in doc.get("claims", []):
        require_semantic_id(claim.get("id"), f"{path}:claim")
        claim_sources = claim.get("sources", [])
        if not claim_sources or any(source not in sources for source in claim_sources):
            raise ValueError(f"{path}: claim has missing source reference")
    return {doc["id"], *sources}


def parse_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError(f"{path}: missing frontmatter")
    head, body = text[4:].split("\n---\n", 1)
    fields: dict[str, object] = {}
    for line in head.splitlines():
        if not line or line.startswith("  - "):
            continue
        if ": " in line:
            key, value = line.split(": ", 1)
            fields[key] = int(value) if value.isdigit() else value
    require_semantic_id(fields.get("id"), f"{path}:id")
    year = fields.get("year")
    if not isinstance(year, int) or not 1769 <= year <= 2026:
        raise ValueError(f"{path}: year out of range")
    if "[^" not in body:
        raise ValueError(f"{path}: narrative requires a source note")
    return fields


def validate_geography(path: Path, known_ids: set[str]) -> None:
    doc = canonical_roundtrip(path)
    if doc.get("type") != "FeatureCollection" or not doc.get("features"):
        raise ValueError(f"{path}: invalid or empty FeatureCollection")
    for feature in doc["features"]:
        require_semantic_id(feature.get("id"), f"{path}:feature")
        props = feature.get("properties", {})
        if props.get("entity") not in known_ids or props.get("source") not in known_ids:
            raise ValueError(f"{path}: unresolved entity/source reference")
        if not all(key in props for key in ("validity", "precision", "confidence")):
            raise ValueError(f"{path}: temporal geography metadata incomplete")


def main() -> None:
    known: set[str] = set()
    entities = sorted((ROOT / "content/entities").glob("*.jsonld"))
    stories = sorted((ROOT / "content/stories").glob("*.md"))
    geography = sorted((ROOT / "content/geography").glob("*.geojson"))
    for path in entities:
        known.update(validate_entity(path))
    for path in stories:
        parse_frontmatter(path)
    for path in geography:
        validate_geography(path, known)
    print(json.dumps({"status": "PASS", "entities": len(entities), "stories": len(stories), "geographies": len(geography), "round_trip": "deterministic"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
