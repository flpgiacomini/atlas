# Heurist Setup Blueprint — A3

## Goal
Use Heurist as a **research/curation workspace**, not as Atlas canonical identity.

The first setup must prioritize round-trip fidelity over a beautiful Heurist-native schema.

## Create only three record types initially
1. Entity
2. Statement
3. Source

Do not create 18 Heurist record types on day one.

### Why
If we immediately reproduce Vehicle, Person, Facility, Circuit, Event, Entry etc. as distinct Heurist schemas,
we would be testing Heurist configuration rather than testing whether the Atlas workflow is pleasant.

`Entity Type` distinguishes them for the first operational cycle.

## Import order
1. `sources_for_heurist.csv`
2. `entities_for_heurist.csv`
3. `statements_for_heurist.csv`

The third import resolves:
- Subject → Entity
- Object Entity → Entity
- Sources → Source

## First saved searches
Create:
- Entities by Type
- Vehicles
- Events
- Entries
- Disputed Statements
- Needs Reconciliation
- Statements without Source
- Sources by Tier
- Current open-ended temporal relationships

## First visual tests
### Network
Filter Entity/Statement records for Porsche 917 and expand:
917 → variant/chassis → Entry → drivers/team → Event.

### Timeline
Use Events and temporal Statements for:
- 911 lineage
- Gurgel corporate events
- Model T production/technology
- Nürburgring layout changes

### Map
Do not build a full geographic model yet.
Map only entities with confirmed Place/geometry data once Place import is normalized.

## Pass criteria
Heurist passes A3 if:
- adding one new Entity takes <2 minutes excluding research;
- adding one sourced Statement is not cumbersome;
- conflicting Statements remain visible;
- export preserves IDs, predicates, validity, confidence and source links;
- network/timeline views require no duplicate data.

## Stop condition
If Statement-as-record makes ordinary data entry clearly unpleasant,
do not spend weeks tuning Heurist.
Test Wikibase next for semantic workflow or Grist for simplicity.
