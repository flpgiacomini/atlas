# A9 Remaining Work

## Complete
- production architecture selected;
- static Astro repository skeleton;
- canonical SQLite exporter;
- static Entity route contract;
- provenance rendered in page model;
- Pagefind build step defined;
- Cytoscape/vis-timeline component scaffolds;
- provider-independent static output contract.

## Next implementation slices

### A9.2 — Geography
Canonicalize Place/Facility coordinates and remove `map-points.prototype.json`.

### A9.3 — Product UX
Port/refine:
- global search modal;
- entity header/summary;
- relationship sections grouped semantically;
- evidence drawer;
- genealogy view;
- compare flow.

### A9.4 — Exploration
- global timeline filters;
- graph expansion/path exploration;
- map layers/time filters.

### A9.5 — Research publication loop
Prove one new researched entity can travel:
Zotero/Heurist/OpenRefine → SQLite → build → deployed page.

### A9.6 — Deployment
Cloudflare Pages build and generic GitHub Pages fallback.

### A9.7 — Product Complete gate
Run real curiosity-driven sessions and fix friction.
