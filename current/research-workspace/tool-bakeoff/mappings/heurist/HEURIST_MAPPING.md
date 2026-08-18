# Heurist Mapping — Atlas five-case pilot

## Recommended test mode: fidelity-first

Create record types:
- Entity
- Statement
- Source

Do **not** reproduce all Atlas entity subtypes as Heurist record types in the first test.
Use `entity_type` as a controlled term first. This keeps the bake-off small and tests semantics rather than UI configuration.

### Entity record fields
- Atlas ID — unique text
- Entity Type — controlled term
- Canonical Name
- Slug
- Metadata JSON — long text for pilot only
- Names JSON — long text for pilot only
- External IDs JSON — long text for pilot only

### Statement record fields
- Atlas Statement ID — unique text
- Subject — record pointer to Entity
- Predicate — controlled term
- Object Type — controlled term
- Object Entity — record pointer to Entity, when object_type=entity
- Literal Value — text/number/date for non-entity objects
- Object Precision
- Valid From / Until
- Valid From / Until Precision
- Qualifiers
- Confidence
- Resolution Status
- Sources — repeated record pointers to Source

### Why this mapping
It preserves Atlas semantics exactly enough to round-trip.

### What to test after import
1. Can Statement records be browsed without making daily research tedious?
2. Can network expansion traverse Statement → Entity clearly enough?
3. Can temporal filtering use the validity fields naturally?
4. Can the 901→911 conflicting dates be shown without overwriting one another?
5. Can a saved visualization hide Statement nodes when presenting the domain graph?

### Potential optimization after bake-off
If Heurist wins, frequent predicates such as `part_of`, `successor_of`, `manufactured_by`, `designed_by`,
`located_in` can be promoted to direct pointer fields while the canonical exporter continues to emit Atlas Statements.

Do not perform that optimization before proving round-trip fidelity.
