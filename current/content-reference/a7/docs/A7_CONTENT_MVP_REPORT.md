# ATLAS — A7 Content MVP Report

## Result
**PASS**

A7 adds a compact continuity layer across the twentieth and early twenty-first centuries.

### Added
- Entities: 67
- Statements: 79
- Sources: 24
- Claims/Evidence: 93 / 93

### Canonical totals
```json
{
  "entity": 334,
  "statement": 439,
  "source": 123,
  "claim": 563,
  "evidence": 563,
  "predicate": 54
}
```

## What A7 closes

### Interwar / pre-war engineering
- Citroën Traction Avant
- Volkswagen Beetle / Type 1 origins-to-postwar production transition

### Post-war reconstruction and utility
- Ferrari 125 S
- Land Rover Series I
- Toyota Land Cruiser BJ

### 1950s–1970s mass-market and architecture
- Classic Mini
- Ford Mustang
- Lamborghini Miura
- Mazda Cosmo Sport
- Volkswagen Golf I

### 1980s–1990s product concepts
- Renault Espace
- McLaren F1

### Electrification / alternative propulsion
- Tesla Roadster
- BYD F3DM
- Toyota Mirai

### Africa as industrial geography
- BMW Group Plant Rosslyn, South Africa

## Content-MVP principle
A7 deliberately does not maximize vehicle count.

The dataset now supports exploration across:
- pioneer vehicles;
- mass production;
- luxury/performance;
- off-road;
- sports/supercars;
- family/MPV;
- rotary;
- FWD architectures;
- BEV;
- PHEV;
- fuel cell;
- manufacturing globalization.

## Gate
- Six inhabited continents represented in meaningful automotive/industrial context: PASS.
- Major eras from 1885 through current-era electrification: PASS.
- New root Entity types required: 0.
- New Predicates required: 0.
- Provenance retained: PASS.
- Canonical SQLite integrity: PASS.

## Interpretation
This is now a **Content MVP**, not merely a semantic test dataset.

It is still intentionally sparse.
A user should be able to move across different eras and automotive ideas without every path ending in Porsche/Ford/pre-1918 content.

## Next phase
**A8 — Architecture Gate**

A8 must decide which parts of the A6 shell and current tooling deserve to become durable:
- canonical database/runtime;
- search;
- API;
- frontend;
- graph/timeline/map rendering;
- deployment;
- research-to-publication pipeline.

The decision must be based on the now-broader A7 content, not on hypothetical future scale.
