# OpenRefine Reconciliation Recipe — Atlas

## Trigger
Use OpenRefine for batch work, not every single manually researched Entity.

Good triggers:
- 20+ candidate entities;
- import from Wikidata/database/catalogue;
- repeated names;
- multilingual names;
- external-ID enrichment;
- duplicate detection.

## Input columns
Minimum:
- candidate_name
- candidate_type
- country/place if known
- date/context if known
- source_id
- source_external_id if present

## Workflow

### 1. Clean
- trim whitespace;
- normalize obvious punctuation;
- preserve original name in a separate column;
- do NOT strip diacritics from canonical display values.

### 2. Reconcile to Wikidata
Use type/context columns when available.

### 3. Review
Never automatically accept all high-score candidates.

Classify:
- exact_identity
- probable_identity
- no_match
- ambiguous
- new_atlas_entity

### 4. External IDs
For accepted matches, add Wikidata QID as External Identifier.

### 5. Atlas reconciliation
Before creating a new Atlas Entity:
- search canonical Atlas IDs;
- compare existing external identifiers;
- compare historical names;
- compare dates/place/context.

### 6. Export
Produce:
- accepted entity updates;
- new entity candidates;
- unresolved reconciliation queue.

## Hard rule
Wikidata reconciliation answers:
"which external entity might this be?"

It does NOT answer:
"should Atlas merge these records?"

Atlas identity remains a curatorial decision.
