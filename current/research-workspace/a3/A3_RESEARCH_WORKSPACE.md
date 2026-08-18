# ATLAS — A3 Research Workspace v0.1

## Status
**PREPARED — UI SETUP REMAINS**

The model and import artifacts are ready.

## Provisional stack
- Zotero — source capture/library
- OpenRefine — batch cleaning + Entity Resolution
- Heurist — research/curation workspace
- Atlas SQLite v1 — canonical portable checkpoint
- JSONL/CSV — interchange

## Important distinction
Research is performed in the workspace.
Canonical validation is performed against the Atlas model.

## What is intentionally not automated yet
- automatic ingestion from every source;
- automatic fact extraction by AI;
- automatic entity merges;
- automatic confidence scoring;
- continuous synchronization between Heurist and SQLite.

Those are optimizations for demonstrated pain, not MVP requirements.

## A3 exit gate
A3 is complete after a hands-on workspace run proves:
1. five-case import;
2. source/statement editing;
3. one conflict preserved;
4. one network view;
5. one timeline view;
6. clean export;
7. successful reconstruction/validation against Atlas SQLite v1.

The UI/account actions themselves must be performed in the chosen Heurist instance.
