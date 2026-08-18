# ATLAS — A9 Product v0.2

## Result
Structural/build-data gate: **PASS**

## Canonical snapshot
- Entities: 339
- Statements: 446
- Sources: 125
- Claims/Evidence: 572 / 572
- Predicates: 54

## A9.2 Geography
Implemented:
- Facility/Place location truth separated from render geometry.
- Selected official addresses captured in a publication geography registry.
- Prototype coordinates explicitly remain `provisional`.
- Production map refuses to render provisional coordinates as canonical.
- No runtime geocoding.

Remaining:
- reconcile geometry/external IDs;
- mark release-ready points/polygons;
- broaden coverage.

## A9.3 Product UX
Implemented in Astro scaffold:
- semantic grouping of relationships;
- evidence/source expansion at fact/relation level;
- compare selection via localStorage;
- compare page;
- map curation queue;
- type metadata/filter markers for Pagefind;
- global nav.

## A9.5 Research → Publication proof
New research was added to the canonical SQLite:
Volvo PV544 → Nils Bohlin → modern three-point safety belt → 13 Aug 1959 Event.

Then `export_web.py` was rerun successfully:
- pages: 339
- graph edges: 332
- timeline events: 103

This proves the publication flow is not hardcoded around A7 content.

## A9.6 Deployment contract
The production artifact remains static `dist/`.
Cloudflare Pages is primary, but no Cloudflare runtime capability is required.

## Remaining blockers before A9 Product Complete
1. real geometry reconciliation;
2. actual Astro/Pagefind install + build;
3. browser visual/product acceptance;
4. polished global timeline/map/graph experience;
5. deployment run from a repository/CI;
6. hands-on research workspace loop with Heurist/Zotero/OpenRefine.
