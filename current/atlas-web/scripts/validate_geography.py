#!/usr/bin/env python3
from pathlib import Path
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
rows = json.loads((ROOT / "data" / "geography.registry.json").read_text(encoding="utf-8"))
errors = []
for row in rows:
    label = row.get("entity_name", "?")
    for field in ("entity_id", "official_address", "address_source", "geometry_source", "geometry_precision", "reviewed_on"):
        if not row.get(field): errors.append(f"{label}: missing {field}")
    if row.get("release_ready"):
        if row.get("geometry_status") != "verified": errors.append(f"{label}: release-ready geometry is not verified")
        if not all(isinstance(row.get(k), (int, float)) and math.isfinite(row[k]) for k in ("lat", "lon")):
            errors.append(f"{label}: invalid coordinates")
result = {"passed": not errors, "errors": errors, "records": len(rows), "release_ready": sum(bool(r.get("release_ready")) for r in rows)}
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0 if not errors else 1)
