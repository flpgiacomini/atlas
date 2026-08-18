#!/usr/bin/env python3
from pathlib import Path
import json
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "data" / "media.manifest.json").read_text(encoding="utf-8"))
allowed = {"Public Domain", "CC0", "CC BY 4.0", "CC BY-SA 4.0"}
errors = []
items = manifest.get("items", [])
by_entity = {}
for item in items:
    by_entity.setdefault(item.get("entity_id"), []).append(item)
    for field in ("entity_id", "file", "creator", "source_url", "license", "license_url", "credit", "alt", "verified_on", "nature"):
        if not item.get(field): errors.append(f"{item.get('entity_id', '?')}: missing {field}")
    if item.get("license") not in allowed: errors.append(f"{item.get('entity_id')}: disallowed license")
    if not (ROOT / "public" / item.get("file", "")).is_file(): errors.append(f"{item.get('entity_id')}: missing file")
db = sqlite3.connect(ROOT / "data" / "atlas.sqlite")
entity_ids = {row[0] for row in db.execute("SELECT id FROM entity")}
db.close()
for entity_id in sorted(entity_ids - set(by_entity)): errors.append(f"{entity_id}: no media")
for entity_id in sorted(set(by_entity) - entity_ids): errors.append(f"{entity_id}: unknown entity")
result = {"passed": not errors, "errors": errors, "entities": len(entity_ids), "covered": len(entity_ids & set(by_entity))}
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0 if not errors else 1)
