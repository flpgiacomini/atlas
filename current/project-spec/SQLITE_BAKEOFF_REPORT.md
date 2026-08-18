# ATLAS — SQLite Bake-Off v0.1

## Result
**PASS after data-quality fixes.**

The five pilots were merged into one canonical SQLite snapshot and representative queries executed successfully.

## What the merge discovered
1. Earlier pilots reused local Claim/Evidence IDs across datasets.
2. Nürburgring v0.1 also contained duplicate Statement IDs.
3. Therefore Atlas v1 requires globally unique/namespaced IDs and duplicate-ID validation before import.
4. `Turbocharging` existed independently in the Porsche 917 and Porsche 911 pilots, demonstrating a real Entity Resolution need.

## Counts
```json
{
  "entity": 86,
  "entity_redirect": 1,
  "statement": 131,
  "claim": 203,
  "evidence": 203,
  "source": 24
}
```

## Entity redirects
```json
{
  "p911:tec_000100": "p917:tec_000001"
}
```

## Representative acceptance queries
```json
{
  "911_generations": [
    {
      "subject_name": "Porsche 911 G-Series"
    },
    {
      "subject_name": "Porsche 911 Original"
    },
    {
      "subject_name": "Porsche 911 Type 964"
    },
    {
      "subject_name": "Porsche 911 Type 991"
    },
    {
      "subject_name": "Porsche 911 Type 992"
    },
    {
      "subject_name": "Porsche 911 Type 993"
    },
    {
      "subject_name": "Porsche 911 Type 996"
    },
    {
      "subject_name": "Porsche 911 Type 997"
    }
  ],
  "911_rename_conflict": [
    {
      "object_date": "1964-10-22",
      "confidence": "disputed",
      "resolution_status": "disputed"
    },
    {
      "object_date": "1964-11-22",
      "confidence": "disputed",
      "resolution_status": "disputed"
    }
  ],
  "917_winning_drivers": [
    {
      "canonical_name": "Hans Herrmann"
    },
    {
      "canonical_name": "Richard Attwood"
    }
  ],
  "gurgel_end_events": [
    {
      "canonical_name": "Gurgel concordata request",
      "object_date": "1993",
      "resolution_status": "accepted"
    },
    {
      "canonical_name": "Gurgel bankruptcy",
      "object_date": "1994-05",
      "resolution_status": "accepted"
    },
    {
      "canonical_name": "Gurgel operations closure reported by Rio Claro",
      "object_date": "1996",
      "resolution_status": "needs_reconciliation"
    }
  ],
  "model_t_facilities": [
    {
      "canonical_name": "Ford Piquette Avenue Plant",
      "validity_from": null,
      "validity_until": "1910"
    },
    {
      "canonical_name": "Ford Highland Park Plant",
      "validity_from": "1910",
      "validity_until": null
    }
  ],
  "nurburgring_layouts": [
    {
      "subject_name": "Nürburgring Gesamtstrecke (1927)"
    },
    {
      "subject_name": "Nürburgring Grand Prix Circuit (1984)"
    },
    {
      "subject_name": "Nürburgring Grand Prix Circuit with AMG Arena (2002)"
    },
    {
      "subject_name": "Nürburgring Nordschleife (1927 configuration)"
    },
    {
      "subject_name": "Nürburgring Nordschleife (current 20.832 km configuration)"
    },
    {
      "subject_name": "Nürburgring Südschleife (1927 configuration)"
    }
  ]
}
```

## Architectural conclusion
SQLite can already act as a portable canonical snapshot and query layer for the current model.

This does **not** make it the preferred research interface.

The project should distinguish:
- research/curation workspace;
- portable canonical export;
- exploration/public interface.

No graph database is justified by the five-case dataset.
