# Wikibase Mapping — Atlas five-case pilot

## Native semantic mapping

Atlas → Wikibase

- Entity → Item
- Predicate → Property
- Statement → Wikibase Statement
- object Entity → Item-valued main snak
- valid_from / valid_until → qualifiers
- confidence / resolution_status → qualifiers
- Atlas Statement ID → qualifier (or external-id field if a statement-id extension is later used)
- Source → Source Item
- Claim/Evidence → Wikibase reference block

This is the closest native mapping among the current candidates.

## Important semantic compression
Atlas separates:
Statement → Claim → Evidence → Source

Wikibase normally stores:
Statement → references

For the bake-off, preserve the Atlas Source as an Item and encode evidence locator fields in the reference block.
A contradictory source is normally represented as a separate conflicting Statement with its own references,
not as a `contradicts` Claim attached to the other Statement.

The canonical exporter must be able to reconstruct Atlas Claim/Evidence objects from Wikibase references.

## OpenRefine workflow
1. Import `items_for_openrefine.csv`.
2. Reconcile existing external IDs/names against Wikidata where useful.
3. Create Atlas Items.
4. Create Properties from `proposed_properties.csv`.
5. Import `statements_for_openrefine.csv`.
6. Align statement columns using an OpenRefine Wikibase schema.
7. Add qualifiers and reference blocks.
8. Export JSON/RDF and test round-trip back to canonical SQLite.

## Critical bake-off questions
- Is editing references for every important fact pleasant enough for a hobby project?
- Is creating/maintaining Properties significantly more work than the value gained?
- Can conflicting statements be understood without SPARQL expertise?
- Can we produce timeline/map/network views without building too much around Wikibase?

If the answer to the last two is no, Wikibase remains an excellent interchange/semantic option but not the primary research workspace.
