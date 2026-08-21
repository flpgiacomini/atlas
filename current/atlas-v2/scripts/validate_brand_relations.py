"""Validate temporal, sourced relations between brands and their operators."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"succeeded-by", "renamed-to", "merged-into", "acquired-by", "rights-acquired-by", "spun-off-to", "market-transition-to", "joined-lineage-of", "became-subbrand-of"}
PRECISIONS = {"day": r"\d{4}-\d{2}-\d{2}", "month": r"\d{4}-\d{2}", "year": r"\d{4}"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate() -> dict:
    doc = load(ROOT / "content/brand-relations.json")
    entities = [load(path) for path in (ROOT / "migration/entities").glob("*.jsonld")]
    entities += [load(path) for path in (ROOT / "content/entities").glob("*.jsonld")]
    entity_ids = {item["id"] for item in entities}
    brand_ids = {item["id"] for item in entities if item.get("type") == "Brand"}
    ids: set[str] = set()
    errors: list[str] = []
    for item in doc.get("relations", []):
        prefix = item.get("id", "<missing>")
        if prefix in ids: errors.append(f"{prefix}: duplicate id")
        ids.add(prefix)
        if item.get("from") not in entity_ids: errors.append(f"{prefix}: unknown source participant")
        if item.get("to") not in entity_ids: errors.append(f"{prefix}: unknown target")
        if item.get("from") == item.get("to"): errors.append(f"{prefix}: self relation")
        if item.get("kind") not in KINDS: errors.append(f"{prefix}: invalid kind")
        precision = item.get("precision")
        if precision not in PRECISIONS or not re.fullmatch(PRECISIONS.get(precision, r"$^"), item.get("validFrom", "")):
            errors.append(f"{prefix}: invalid temporal precision")
        if not item.get("label") or not item.get("continuity"): errors.append(f"{prefix}: editorial label and continuity required")
        source = item.get("source", {})
        parsed = urlparse(source.get("url", ""))
        if parsed.scheme != "https" or not parsed.netloc: errors.append(f"{prefix}: invalid source URL")
        if source.get("trust") != "primary": errors.append(f"{prefix}: primary source required")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", source.get("verifiedAt", "")): errors.append(f"{prefix}: verifiedAt required")
    if errors:
        raise SystemExit("\n".join(errors))
    return {"status": "PASS", "relations": len(ids), "participants": len({value for item in doc["relations"] for value in (item["from"], item["to"])})}


if __name__ == "__main__":
    print(json.dumps(validate(), sort_keys=True))
