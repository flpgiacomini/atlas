"""Validate sourced brand lifecycle milestones without conflating brands and operators."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"founded", "operator-founded", "launched", "trademark-registered", "predecessors-merged", "revived", "renamed", "discontinued", "acquired"}
SCOPES = {"brand-identity", "operator", "ownership"}
PRECISIONS = {"day", "month", "year", "circa"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate() -> dict:
    doc = load(ROOT / "content/brand-timeline.json")
    entity_docs = [load(path) for path in (ROOT / "migration/entities").glob("*.jsonld")]
    entity_docs += [load(path) for path in (ROOT / "content/entities").glob("*.jsonld")]
    entity_ids = {item["id"] for item in entity_docs}
    brand_ids = {item["id"] for item in entity_docs if item.get("type") == "Brand"}
    source_ids = {item["id"] for item in load(ROOT / "migration/sources.jsonld")["items"]}
    ids: set[str] = set()
    errors: list[str] = []
    for item in doc.get("milestones", []):
        prefix = item.get("id", "<missing>")
        if prefix in ids: errors.append(f"{prefix}: duplicate id")
        ids.add(prefix)
        if item.get("brand") not in brand_ids: errors.append(f"{prefix}: unknown or non-Brand entity")
        if item.get("event") and item["event"] not in entity_ids: errors.append(f"{prefix}: unknown event")
        if item.get("kind") not in KINDS: errors.append(f"{prefix}: invalid kind")
        if item.get("scope") not in SCOPES: errors.append(f"{prefix}: invalid scope")
        if item.get("precision") not in PRECISIONS: errors.append(f"{prefix}: invalid precision")
        if not isinstance(item.get("year"), int) or not 1769 <= item["year"] <= 2026: errors.append(f"{prefix}: invalid year")
        date = item.get("date", "")
        if item.get("precision") == "day" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date): errors.append(f"{prefix}: day precision requires YYYY-MM-DD")
        if item.get("precision") == "month" and not re.fullmatch(r"\d{4}-\d{2}", date): errors.append(f"{prefix}: month precision requires YYYY-MM")
        if date and not date.startswith(str(item.get("year"))): errors.append(f"{prefix}: date/year mismatch")
        refs = item.get("sourceRefs", [])
        for ref in refs:
            if ref not in source_ids: errors.append(f"{prefix}: unknown source {ref}")
        source = item.get("source")
        if not refs and not source: errors.append(f"{prefix}: source required")
        if source:
            parsed = urlparse(source.get("url", ""))
            if parsed.scheme != "https" or not parsed.netloc: errors.append(f"{prefix}: invalid source URL")
            if source.get("trust") != "primary": errors.append(f"{prefix}: seed sources must be primary")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", source.get("verifiedAt", "")): errors.append(f"{prefix}: external source requires verifiedAt")
    if errors:
        raise SystemExit("\n".join(errors))
    return {"status": "PASS", "milestones": len(ids), "brands": len({item["brand"] for item in doc["milestones"]})}


if __name__ == "__main__":
    print(json.dumps(validate(), sort_keys=True))
