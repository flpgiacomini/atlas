# ATLAS — A9 Implementation Plan after Architecture Gate

A8 freezes the production architecture. A9 is no longer an architecture exercise.

## A9.1 Web foundation
- Create Astro static project.
- Define Entity route `/e/[id-or-slug]/`.
- Port A6 visual language into reusable Astro components.
- Keep zero framework islands initially.

## A9.2 Build adapter
Create one deterministic `atlas export web` step:
- validate canonical SQLite;
- export build-time entities/statements/sources;
- derive graph/timeline/map projections;
- fail build on integrity errors.

## A9.3 Search
- Generate all Entity pages.
- Run Pagefind after Astro build.
- Add type filters and aliases.
- No external search service.

## A9.4 Entity experience
Required:
- identity/header;
- historical summary;
- key facts;
- relationships;
- genealogy;
- related events;
- technologies/components;
- Motorsport;
- evidence/source drawer;
- external IDs.

Hide internal data-model ceremony unless the user opens evidence/debug details.

## A9.5 Exploration surfaces
- graph: Cytoscape.js;
- timeline: vis-timeline;
- map: Leaflet;
- compare: generated compact compare index.

## A9.6 Geography
Replace A6/A7 approximate map points with curated canonical Place/Facility coordinates and external identifiers.
Prototype coordinates must be deleted from the release build.

## A9.7 Research-to-publication
Prove:
Zotero/Heurist/OpenRefine → canonical SQLite → validation → static build.

No manual copying into the web repository.

## A9.8 Quality
- accessibility pass;
- responsive desktop/mobile browser layouts;
- broken-link validation;
- provenance checks;
- performance budget;
- offline-friendly static pages where practical.

## A9.9 Deployment
- Cloudflare Pages primary.
- Build output must also run under a generic local static server.
- No Pages Functions/Workers required.
- Document GitHub Pages fallback.

## A9.10 Product Complete gate
A9 completes when the following are true:
1. real research can enter canonical data;
2. canonical build passes automatically;
3. site deploys from scratch;
4. search works;
5. entity exploration works;
6. graph/timeline/map work;
7. evidence is visible;
8. compare works;
9. no runtime server is required;
10. user can use the Atlas for actual curiosity-driven sessions rather than demo paths.

After that: v1.x content/quality lifecycle.
