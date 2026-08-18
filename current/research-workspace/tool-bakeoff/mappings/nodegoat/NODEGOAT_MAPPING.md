# nodegoat Mapping — Atlas five-case pilot

## Technical fit
nodegoat supports:
- custom relational data models;
- temporal contexts and Chronology Statements;
- source references down to Object Description level;
- conflicting/uncertain historical information;
- CSV relational import;
- spatial and diachronic network visualisations;
- CSV/ODT export and JSON/JSON-LD via API on applicable deployments.

## Recommended bake-off model
Use three principal Object Types:
- Entity
- Statement
- Source

As with Heurist, begin fidelity-first.

Statement:
- Atlas Statement ID
- Subject reference
- Predicate classification
- Object Entity reference OR literal value
- temporal validity / chronology
- confidence
- resolution status
- source references

## Why not immediately map every predicate to Object Descriptions?
Doing so would make nodegoat visually elegant but would bind the Atlas ontology tightly to nodegoat's model.
First prove that the canonical model can round-trip.

## Operational blocker
Current nodegoat.net terms state that registration is limited to researchers and academics.
The Atlas is a personal non-academic project, so free hosted access must **not** be assumed.

The open-source software can be self-hosted, but that introduces infrastructure we are deliberately avoiding.
The free hosted tier also does not include API/public front-end according to the current product table.

Therefore:
- retain nodegoat as the functional benchmark;
- test only if account eligibility is confirmed or self-hosting later becomes acceptable.
