# A3 Export & Backup Routine

## Canonical principle
The curation workspace is replaceable.

## During active research
- Zotero keeps source library.
- Heurist contains working structured records.
- Atlas SQLite snapshots are generated at checkpoints.

## Checkpoint frequency
Create a canonical export:
- after a significant research batch;
- before changing Heurist schema;
- before bulk import/reconciliation;
- before starting a new historical chapter.

No daily ceremony is required for a personal project.

## Checkpoint contents
- canonical SQLite
- JSONL export
- Predicate Registry
- migration/external-ID maps
- source registry
- validation report

## Validation gate
Do not call an export canonical when:
- foreign keys fail;
- duplicate canonical IDs exist;
- a Claim lacks Evidence;
- an Evidence lacks Source;
- new Predicates bypass the registry.

## Git
Store schemas, registries, scripts and documentation in Git.

Do not put a rapidly changing large Zotero attachment library into Git.
