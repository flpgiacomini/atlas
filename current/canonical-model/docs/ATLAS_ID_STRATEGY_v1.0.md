# ATLAS ID Strategy v1.0

## Canonical ID
UUIDv7 for Entity, Predicate, Statement, Claim, Evidence and Source.

## Human-readable identity
Use canonical_name and mutable slug. Never use slug as a foreign key.

## External identity
Wikidata, OSM, FIA, Racing Sports Cars, manufacturer IDs and other databases are stored in `external_identifier`.

## Migration
Pilot IDs are retained in `legacy_identifier`.
Merges preserve redirects/migration lineage instead of silently reusing identifiers.
