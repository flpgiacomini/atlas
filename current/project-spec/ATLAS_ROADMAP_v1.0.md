# ATLAS — Roadmap v1.0

## A0 — Scope Freeze
**STATUS: COMPLETE**

Deliverables:
- semantic scope frozen;
- five pilot models validated;
- hard out-of-scope list;
- change-control rules.

Gate:
No additional domain is added before implementation validation.

---

## A1 — Research Workspace Bake-Off
**STATUS: IN PROGRESS**

Candidates:
1. nodegoat
2. Heurist
3. Wikibase
4. Grist fallback

Supporting tools:
- Zotero
- OpenRefine

Use exactly the five validated pilots. Do not create new content for this phase.

Gate:
A research workflow can create, edit, reconcile, source, query and export Atlas knowledge without custom software.

---

## A2 — Canonical Data Model v1.0
Tasks:
- global ID strategy;
- namespace/import rules;
- Predicate Registry;
- JSON/YAML interchange contract;
- SQLite canonical snapshot schema;
- validation rules;
- Entity Resolution rules;
- conflict/reconciliation states.

Gate:
All five pilots merge cleanly with zero duplicate IDs, zero dangling references and reproducible acceptance queries.

---

## A3 — Research Workspace Operational
Tasks:
- configure Zotero collections/tags;
- define Source Registry conventions;
- define OpenRefine reconciliation workflow;
- configure chosen curation workspace;
- establish backup/export routine;
- define lightweight research checklist.

Gate:
A new entity can move from discovery → source → reconciliation → curated Statement/Evidence without manual duplication across unrelated tools.

---

## A4 — Seed Dataset
Do not optimise for raw vehicle count.

Build a deliberately diverse corpus covering:
- early pioneers;
- production vehicles;
- race cars;
- prototypes/concepts;
- mass-market cars;
- extinct manufacturers;
- corporate genealogy;
- platform/component sharing;
- several countries/continents;
- circuit evolution;
- technological change.

Gate:
The data model remains stable under diversity, not just Porsche/Ford-style cases.

---

## A5 — Chapter I: 1885–1918
First real historical scaling test.

Research:
- Germany
- France
- United Kingdom
- Italy
- United States
- additional relevant early industries discovered during research

Deliverables:
- manufacturers;
- founders/engineers;
- vehicles;
- early technologies;
- factories/places;
- corporate relationships;
- key events;
- sources and uncertainty.

Gate:
The period is meaningfully explorable through entities and relations. Completeness is not required.

---

## A6 — Exploration Prototype
Only now create the minimum custom experience if existing tools are insufficient.

Required surface:
- search;
- entity page;
- relation links;
- source/evidence drawer;
- basic graph;
- timeline;
- map.

Not required:
- polished visual identity;
- mobile app;
- 3D;
- account system.

Gate:
Porsche 917 → chassis → Entry → driver → event → circuit → layout can be navigated in one experience.

---

## A7 — Global Content MVP
Expand by historical coverage rather than volume.

Coverage matrix:
- eras;
- regions;
- vehicle roles;
- manufacturers active/extinct;
- technologies;
- Motorsport;
- corporate consolidation.

Gate:
The Atlas feels global and historically varied, not like a collection of famous European sports cars.

---

## A8 — Architecture Gate
Only here decide whether custom infrastructure is justified.

Questions:
- Is the research workspace limiting curation?
- Is SQLite limiting queries?
- Are graph traversals genuinely difficult?
- Do map/timeline views require a custom backend?
- Is a custom API necessary?
- Is existing software creating more friction than it removes?

Possible outcomes:
- keep current tools;
- PostgreSQL;
- embedded graph engine;
- Wikibase as canonical KG;
- custom application.

Neo4j remains an option, not a destination.

---

## A9 — Atlas v1
A personal, maintainable, navigable historical automotive atlas.

Success means:
- useful for real curiosity-driven exploration;
- provenance visible;
- conflicting history represented honestly;
- data portable;
- research remains enjoyable;
- infrastructure remains smaller than the research problem.
