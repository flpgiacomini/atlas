# ATLAS — A8 Architecture Gate Decision v1.0

## Decision
**A8 PASS: Atlas v1 will be static-first and backendless in production.**

The A7 content snapshot was successfully projected into:
- 334 static Entity pages;
- a static search index;
- a static global graph index;
- a static timeline;
- a separate map layer;
- source/evidence content rendered directly into Entity pages.

No FastAPI/Datasette runtime is required to publish or explore the v1 content.

## Durable architecture

```text
RESEARCH
Zotero + OpenRefine + Heurist (provisional)
            │
            ▼
CANONICAL BUILD
Atlas SQLite v1
            │
            ├── validation
            ├── source/evidence checks
            └── export/build
            │
            ▼
PUBLICATION
Astro static build
├── Entity pages
├── relationship data
├── timeline data
├── graph data
├── GeoJSON/map data
└── Pagefind index
            │
            ▼
STATIC HOST
Cloudflare Pages (primary)
GitHub Pages / any static host (fallback)
```

## Why no production backend
Current product requirements are overwhelmingly read-only:
- search;
- page rendering;
- relation traversal;
- graph;
- timeline;
- map;
- evidence;
- compare.

All can be generated or calculated in the browser from immutable build artifacts.

A backend would currently add:
- hosting;
- patching;
- runtime availability;
- API versioning;
- database exposure;
- caching;
without adding user value.

## Frontend decision
**Astro static output + TypeScript/vanilla client scripts.**

Do not adopt React/Vue/Svelte for the whole application.

Interactive islands remain ordinary JS/TS unless a specific component becomes complex enough to justify a framework island.

Why Astro:
- static is the default output model;
- dynamic Entity routes can be enumerated at build time;
- build-time TypeScript is available;
- interactive scripts can remain vanilla;
- no server adapter is required for a static site.

## Search
**Pagefind.**

Reason:
- indexes generated static HTML after build;
- requires no hosted search service;
- custom JS API is available;
- supports filtering and multilingual sites if needed later.

A7's 334-entity proof uses a small JSON index only because Pagefind is not installed in this execution environment.
Replace it with Pagefind in A9.

## Canonical SQLite in the browser?
**No for normal navigation.**

SQLite WASM and Datasette Lite both demonstrate that SQLite can run/explore entirely inside the browser,
but loading a database engine for every normal visitor is unnecessary when pages can be pre-rendered.

Keep:
- SQLite WASM as a future power-user/offline analysis option;
- Datasette Lite as a zero-server data-inspection option.

Do not make either a v1 page-rendering dependency.

## API
**No public API required in v1.**

Build artifacts are the interface:
- HTML
- JSON
- GeoJSON

If an API becomes useful after A9, expose it from the same canonical data contract rather than making the UI depend on it.

## Graph
**Cytoscape.js stays.**

Canonical storage remains Statements in SQLite.
Build produces compact graph projections.
No Neo4j.

## Timeline
**vis-timeline stays.**

Timeline records are derived from Event/date Statements at build time.

## Map
**Leaflet stays for v1.**

Reasons:
- current map needs markers and simple historical/industrial locations;
- it is substantially simpler than vector-tile infrastructure.

Basemap/provider is configurable.

Future gate:
move to MapLibre + PMTiles only when historical geometries, vector styling, large datasets or provider independence make it valuable.

## Research/admin
**Datasette is local/diagnostic only.**
It can expose the canonical SQLite as a read-only browser/JSON API when useful.

**Heurist remains provisional authoring workspace.**
It is replaceable. The publication pipeline depends only on canonical Atlas exports.

## Hosting
### Primary: Cloudflare Pages
Static assets require no Functions.
This preserves a R$0 runtime path and requires no always-on server.

### Fallback: GitHub Pages or any static host
The output is ordinary HTML/CSS/JS/JSON.
Cloudflare-specific runtime features are forbidden in v1 unless a later requirement proves them necessary.

## Scaling gates
Static architecture remains default until a measured limit appears.

Re-open backend decision only if one of these becomes true:
1. private multi-user editing is required in the public app;
2. personalized state must sync across devices;
3. dynamic queries cannot reasonably be precomputed/client-side;
4. build time becomes operationally painful;
5. entity/page volume approaches host file limits;
6. frequently changing data makes rebuild latency unacceptable.

None is true today.

## Repository separation
Recommended:

`atlas-research` (private)
- schema
- canonical build scripts
- source registry/export
- SQLite snapshots/releases
- validation

`atlas-web`
- Astro UI
- generated publication data during CI
- static deployment configuration

No database credentials exist in the web project.

## A8 result
Architecture is now intentionally boring:

**curate → validate → build → static deploy.**

This is a feature.
