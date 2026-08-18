# ATLAS — Scope Freeze v1.0

## Status
**FROZEN FOR IMPLEMENTATION VALIDATION**

The semantic scope is now closed after validation with:
- Porsche 917
- Porsche 911
- Gurgel BR-800
- Ford Model T
- Nürburgring

A new idea does not enter v1 merely because it is interesting.

## Product definition
Atlas is a global, historical and explorable atlas of the automotive industry, centered on vehicles and represented as a temporal network of entities, statements, events and evidence.

## Semantic primitives
- Entity
- Statement
- Event (Entity subtype)
- Entry (Entity subtype)
- Claim
- Evidence
- Source
- Predicate

There is no separate Relationship primitive. Entity-to-entity Statements are graph edges.

## Entity types frozen for v1
- Vehicle
- VehicleInstance
- Organization
- Brand
- Person
- Technology
- Component
- Facility
- Place
- Competition
- Season
- Team
- Circuit
- CircuitLayout
- Regulation
- Event
- Entry

## Vehicle granularity
Vehicle uses `vehicle_level`:
- family
- generation
- variant
- configuration
- standalone

Do not create separate root schemas for Family, Generation, Variant or Configuration.

## Experiences in scope
- entity page
- search/discovery
- relation exploration
- graph view
- timeline
- map
- genealogy
- comparison
- source/evidence inspection

Timeline, map, graph, genealogy and comparison are derived views, not parallel databases.

## Evidence in scope
Every important historical statement must be capable of carrying:
- provenance
- source
- evidence locator
- confidence
- conflict/reconciliation status

Primary sources are not automatically treated as infallible.

## Temporal scope
- historical
- current
- officially announced/planned

Future items must distinguish announced/planned/scheduled from occurred/existing.

## Geography
Global. Place is the geographic primitive. Atlas will not reproduce a world geographic database.

## Content completeness
Complete in context, not exhaustive in every technical configuration.

## Hard out-of-scope for v1
- 3D vehicle models
- hosted video library
- telemetry and lap-by-lap data
- exhaustive VIN catalogue
- every model year / trim / option combination
- complete parts catalogue
- proprietary map engine
- proprietary graph engine
- mobile app
- social/community platform
- complex authentication
- graph database as an architectural requirement
- indiscriminate automatic ingestion
- AI deciding historical truth automatically

## New data-quality rules discovered by the pilots
1. IDs must be globally unique or namespaced before canonical import.
2. Every collection must reject duplicate IDs.
3. Entity Resolution is mandatory before canonical merge.
4. Exact-name equality is not sufficient for identity, but is a reconciliation signal.
5. Generation editorial periods must not be treated as exact production periods.
6. Corporate bankruptcy, insolvency, operations end, legal dissolution and brand discontinuation are distinct.
7. VehicleInstance may change configuration over time/context.
8. Circuit length belongs to CircuitLayout/configuration, not globally to Circuit.
9. Official sources may conflict and both claims must remain traceable.

## Change-control rule
A new Entity type may be added only when:
1. at least two real cases require it;
2. Entity + Statement + qualifier + Event + Entry cannot represent the cases cleanly;
3. the distinction materially improves research, queries or navigation.

A new Predicate may be added only when:
1. no existing predicate has the same meaning;
2. a qualifier is insufficient;
3. at least one real case exists, preferably two.

## Scope gate
Any proposed addition must answer:
**Does this materially improve understanding or exploration of automotive history?**
If not, it remains outside v1.
