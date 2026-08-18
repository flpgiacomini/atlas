# ATLAS — Tool Bake-Off Decision v0.1

## Key architectural split
Do not force one product to do everything.

Atlas tooling is separated into:
1. Research capture
2. Entity reconciliation / cleaning
3. Research & curation workspace
4. Canonical portable snapshot
5. Exploration/publication layer

## Tier A — Test first

### nodegoat — FIRST HANDS-ON TEST
Why:
- designed for historical/humanities research;
- custom data models;
- relational, temporal and spatial analysis;
- uncertain/conflicting chronology support;
- source references;
- network visualisation;
- hosted accounts available for individual research projects;
- API/export/publication capabilities.

Risk:
- its internal research model may not map cleanly enough to Atlas Statement/Claim/Evidence;
- workflow/UX must be tested with the five-case dataset;
- should not become an irreversible source of truth without export tests.

Provisional role:
**Research/curation workspace candidate #1.**

### Heurist — SECOND HANDS-ON TEST
Why:
- specifically designed for richly structured Humanities databases;
- user-defined records and relationships;
- maps, timelines and network visualisations;
- open-source;
- strong fit for heterogeneous historical data.

Risk:
- Claim/Evidence semantics may require adaptation;
- interface and deployment model need practical evaluation.

Provisional role:
**Research/curation workspace candidate #2.**

### Wikibase / Wikibase Cloud — SEMANTIC CONTROL TEST
Why:
- Items / Properties / Statements;
- qualifiers;
- references;
- external identifiers;
- RDF/SPARQL ecosystem;
- close conceptual match to Atlas.

Risk:
- heavier mental and operational model;
- weaker integrated historical-map/timeline experience;
- could make a personal hobby feel like maintaining a mini-Wikidata.

Provisional role:
**Semantic graph candidate / control benchmark.**

## Tier B — Supporting tools

### Zotero — ADOPT
Role:
- source library;
- bibliographic metadata;
- web/PDF capture;
- local snapshots where useful;
- source organisation.

Not canonical automotive data.

### OpenRefine — ADOPT
Role:
- data cleaning;
- name normalisation;
- Wikidata/Wikibase reconciliation;
- bulk entity-resolution workflow;
- import preparation.

The five-pilot merge already proved Entity Resolution is needed.

### SQLite — ADOPT AS PORTABLE CANONICAL SNAPSHOT
The five pilots successfully merged into SQLite after quality corrections.

Role:
- portable export;
- reproducible queries;
- validation;
- backup/interchange;
- future application seed.

SQLite is not automatically the human research UI.

### Datasette — KEEP
Role:
- near-zero-development exploration of SQLite;
- filtering;
- facets;
- full-text search;
- JSON API;
- custom SQL.

Useful before a custom Atlas frontend exists.

## Tier C — Fallback / later

### Grist
Excellent relational spreadsheet/database UI and self-hosted community edition.
Keep as the simple fallback if nodegoat/Heurist/Wikibase are too cumbersome.

### Baserow
Viable API-first open-source database UI, but currently offers less domain-specific value than nodegoat/Heurist.

### Omeka S
Strong candidate for a future digital-museum/publication layer:
linked data, exhibits, mapping and timeline modules.
Not preferred as the canonical research model.

### Gephi / Sigma.js / Cytoscape.js
Graph analysis/rendering tools, not canonical databases.

### Leaflet / MapLibre / PMTiles
Map rendering stack, only when a custom exploration interface exists.

### TimelineJS / vis-timeline
Timeline presentation components, not data stores.

## Deferred

### ResearchSpace
Semantically powerful cultural-heritage knowledge graph environment, but likely introduces more conceptual and operational complexity than needed for the personal Atlas at this stage.

### Neo4j / other graph servers
No evidence from the five-case validation requires them.

## Bake-off acceptance test
Import the same five-case dataset and perform:
1. create/edit a Vehicle;
2. create temporal ownership/relationship;
3. register two conflicting claims;
4. attach source/evidence;
5. represent Porsche 917 chassis Entry;
6. represent Porsche 911 generation genealogy;
7. filter entities by time;
8. display/map a Place;
9. explore a network;
10. export all data without semantic loss.

## Decision rule
Choose the simplest candidate that passes at least 8/10 without forcing Atlas semantics into awkward workarounds.

If nodegoat passes, do not build a research CMS.
If Heurist passes better, use Heurist.
If neither preserves Claim/Evidence adequately, test Wikibase.
If all three are too burdensome, use Grist + canonical SQLite.
