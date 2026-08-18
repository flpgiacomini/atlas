# ATLAS — Canonical Data Model v1.0

## Status
**FROZEN FOR A3/A4**

## Canonical primitives
- Entity
- Predicate
- Statement
- Claim
- Evidence
- Source

Event and Entry are Entity types. A relationship is an Entity-valued Statement.

## Entity types
vehicle, vehicle_instance, organization, brand, person, technology, component, facility, place,
competition, season, team, circuit, circuit_layout, regulation, event, entry.

## Vehicle levels
family, generation, variant, configuration, standalone.

No separate root tables for VehicleFamily, Generation, Variant or Configuration.

## Identity
Canonical IDs are UUIDv7. Type, slug and external IDs are independent fields.
Tool-specific IDs never replace Atlas IDs.

## Statement
A Statement contains:
- subject Entity
- controlled Predicate
- typed object
- optional temporal validity
- qualifiers
- confidence
- resolution status

Object types:
entity, string, date, number, quantity, boolean.

## Temporal policy
Never create artificial precision.
Validity is different from occurrence.
Events model occurrences; valid_from/valid_until model relationship validity.

## Provenance
Statement → Claim → Evidence → Source.

Claims can support, contradict, qualify or merely mention a Statement.
Evidence identifies the exact location within a Source.

## Derived views
Timeline, map, graph, genealogy and comparison are projections.
They do not create parallel canonical records.

## Canonical portability
SQLite is the reference physical implementation for A2/A3.
CSV/JSONL are interchange formats.
Heurist/Wikibase/Grist remain replaceable curation interfaces.
