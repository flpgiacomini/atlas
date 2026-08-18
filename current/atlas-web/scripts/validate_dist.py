from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/"dist"
GEN=ROOT/"src"/"data"/"generated"
errors=[]

if not DIST.exists(): errors.append("dist missing")
pages=json.loads((GEN/"entity-pages.json").read_text(encoding="utf-8"))
for p in pages:
    expected=DIST/"e"/p["id"]/"index.html"
    if not expected.exists():
        errors.append(f"missing entity page: {p['name']} {p['id']}")
        if len(errors)>20: break

for rel in [
    "index.html",
    "timeline/index.html",
    "graph/index.html",
    "map/index.html",
    "compare/index.html",
    "pagefind/pagefind.js",
    "data/graph-index.json",
    "data/compare-index.json",
]:
    if not (DIST/rel).exists(): errors.append(f"missing dist artifact: {rel}")

result={"passed":not errors,"errors":errors,"expected_entity_pages":len(pages)}
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if not errors else 1)
