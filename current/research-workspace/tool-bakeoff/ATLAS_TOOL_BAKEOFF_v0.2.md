# ATLAS — Tool Bake-Off v0.2
## Evidence-based pre-selection

## Result of this round

The tool decision is now split into two questions:

1. **What is the best research/curation workspace?**
2. **What is the safest canonical/portable representation?**

The answer does not need to be the same product.

### Canonical portable representation
**KEEP SQLite + CSV during A1/A2.**

The five-case merge already demonstrates that the Atlas semantic model can be represented and queried in SQLite.
Changing the canonical authority now would create unnecessary migration risk.

### Research workspace — revised test order

1. **Heurist — test first**
2. **Wikibase / Wikibase Cloud — semantic control test**
3. **nodegoat — conditional test**
4. **Grist — fallback**

---

# Why Heurist moves to first place

Heurist currently offers the best operational compromise for this project:

- built specifically for humanities/historical research;
- flexible record types and relationships;
- map + timeline + network visualisation;
- faceted search;
- CSV/TSV import;
- JSON/XML/KML/dump exports;
- built-in publication options;
- import tooling includes bibliographic integrations such as Zotero;
- open-source GPL;
- free non-commercial research services are available.

The main uncertainty is not functionality.
It is whether Atlas' Statement/Claim/Evidence model is comfortable to curate in Heurist.

This is what the mapping files are designed to test.

---

# Why Wikibase is not automatically first

Wikibase is the strongest semantic match:

Atlas:
Entity → Statement → qualifiers → evidence/source

Wikibase:
Item → Statement → qualifiers → references

It supports conflicting values and source references natively, and OpenRefine has current Wikibase reconciliation/upload support.

However, the project is not merely a knowledge graph.
It is a personal historical exploration workspace.

The risks are:
- property administration;
- wiki-style editing friction;
- SPARQL dependence for richer exploration;
- maps/timelines/networks are less integrated into the normal research workflow;
- Wikibase Cloud has a hosting policy and should not be treated as unrestricted generic free hosting.

Therefore Wikibase must prove that semantic elegance does not make the hobby less pleasant.

---

# Why nodegoat is conditional

Functionally, nodegoat is arguably the best fit:
- historical uncertainty;
- conflicting information;
- source references per field;
- complex chronology;
- diachronic maps and networks;
- relational CSV import/export.

But its current hosted-free terms explicitly restrict registration to researchers and academics.
The free hosted plan also lacks API and a public front-end.

Self-hosting is possible because nodegoat is AGPL open source, but adding a server solely to use the research workspace violates the current simplicity goal.

So nodegoat remains the benchmark, not the default.

---

# Why Grist remains important

If Heurist and Wikibase both make data entry feel bureaucratic, use Grist.

That is not a failure.
It is the explicit simplicity escape hatch.

The Atlas can remain:
Zotero → OpenRefine → Grist → canonical SQLite

and receive custom visualisations only when the content justifies them.

---

# 10-point bake-off protocol

Each research-workspace candidate must demonstrate:

1. Create/edit Vehicle.
2. Create temporal relationship.
3. Store both official 901→911 rename dates without silent overwrite.
4. Associate source/evidence with the facts.
5. Represent Porsche 917 Entry with chassis/team/drivers/result.
6. Represent Porsche 911 generation genealogy.
7. Filter/query by time.
8. Place entities on a map.
9. Explore a relationship network.
10. Export enough information to reconstruct the canonical SQLite model.

### Gate
- **8/10 minimum**
- no critical semantic loss
- no recurring workflow that feels substantially heavier than maintaining the data itself

---

# Scores are not the decision

The numerical scorecard is an aid, not a formula.
nodegoat scores highly functionally but is operationally constrained.
Wikibase scores highest semantically but has workflow friction.
Heurist currently appears the best balance.

The actual winner is the product that makes the five-case dataset easiest to maintain **without corrupting or obscuring the Atlas model**.

---

# New supporting-tool findings

### Tropy
Potentially useful later for photographs of archival research material, catalogues, museum labels and period documents.
It is not a replacement for Zotero.

### CollectiveAccess
Useful if the Atlas grows into a museum/archival collection publication project.
Too collection-centric for the canonical knowledge graph.

### Arches
Excellent heritage/geospatial platform but too operationally heavy.

### Recogito
Interesting for text/image annotation and historical place identification.
Use only if source annotation becomes a recurring bottleneck.

---

# Immediate next action

Run a **real UI test** of the five-case import in Heurist first.

Do not add new vehicle cases before completing that test.

If Heurist passes:
- adopt it provisionally for A3 Research Workspace;
- freeze Data Model v1.0;
- begin Chapter I.

If Heurist fails specifically on Statement/Evidence:
- run the exact same test in Wikibase.

If Wikibase is semantically excellent but unpleasant for research:
- use Grist as workspace and keep SQLite as canonical.

nodegoat returns to first consideration if hosted eligibility is confirmed or self-hosting later becomes acceptable.
