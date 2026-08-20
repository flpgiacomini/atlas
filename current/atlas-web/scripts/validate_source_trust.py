#!/usr/bin/env python3
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
registry = json.loads((ROOT / "data" / "source-trust.registry.json").read_text(encoding="utf-8"))
errors = []
source_ids = [item.get("id") for item in registry.get("sources", [])]
if len(source_ids) != len(set(source_ids)):
    errors.append("duplicate source trust id")
for item in registry.get("sources", []):
    for field in ("id", "name", "mode", "license_status", "confidence"):
        if item.get(field) in (None, "", []):
            errors.append(f"{item.get('id', '?')}: missing {field}")
    if not isinstance(item.get("allowed_fields"), list):
        errors.append(f"{item.get('id', '?')}: allowed_fields must be a list")

db = sqlite3.connect(ROOT / "data" / "atlas.sqlite")
catalog = list(db.execute("SELECT id,metadata_json FROM entity WHERE json_extract(metadata_json,'$.editorial_level')='catalog'"))
attributed = {row[0] for row in db.execute("SELECT entity_id FROM external_identifier WHERE scheme IN ('atlas-brand-census','atlas-significance-candidate')")}
db.close()
for entity_id, raw in catalog:
    metadata = json.loads(raw)
    for field in ("catalog_source", "editorial_batch", "relevance_score", "promotion_state"):
        if metadata.get(field) in (None, ""):
            errors.append(f"{entity_id}: missing {field}")
    if entity_id not in attributed:
        errors.append(f"{entity_id}: missing catalog attribution")

result = {"passed": not errors, "errors": errors, "trusted_sources": len(source_ids), "catalog_records": len(catalog), "attributed": len(attributed & {row[0] for row in catalog})}
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0 if not errors else 1)
