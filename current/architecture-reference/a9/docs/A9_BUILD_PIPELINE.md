# A9 Build Pipeline Contract

## Source
`data/atlas.sqlite` is a validated canonical snapshot.

## Step 1 — Export
`python scripts/export_web.py`

Outputs:
- `src/data/generated/entity-pages.json`
- `src/data/generated/stats.json`
- `src/data/generated/timeline.json`
- `public/data/graph-index.json`
- `public/data/timeline.json`
- prototype map data while geography is unfinished

The exporter is deterministic with respect to the SQLite snapshot.

## Step 2 — Static rendering
Astro `getStaticPaths()` generates one `/e/<UUID>/` route per Entity.

No entity page performs a database query at runtime.

## Step 3 — Search
Pagefind indexes the completed `dist/` HTML tree.

The web application therefore does not maintain a second manually-written search corpus.

## Step 4 — Deploy
Publish `dist/`.

Cloudflare Pages is primary, but the artifact is ordinary static output.

## Failure policy
The production CI must stop before `astro build` if:
- Atlas structural validation fails;
- export produces missing entities/references;
- source/evidence invariants fail.

## Later A9 work
- replace prototype geography with canonical Place/Facility geometry;
- port polished graph/timeline/map/compare components;
- accessibility/responsive pass;
- deployment workflow;
- manual product acceptance.
