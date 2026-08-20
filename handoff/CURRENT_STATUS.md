# ATLAS — estado atual

**Data:** 20/08/2026

**Fase:** expansão pós-v1 — Fase 0 do programa de conclusão integral pronta para execução

**Implementação vigente:** `current/atlas-web/`
**URL:** <https://flpgiacomini.github.io/atlas/>

## Source of truth

1. Escopo: `current/project-spec/ATLAS_SCOPE_FREEZE_v1.0.md`
2. Modelo: `current/canonical-model/docs/ATLAS_CANONICAL_DATA_MODEL_v1.0.md`
3. SQLite: `current/atlas-web/data/atlas.sqlite`
4. Predicate Registry: `current/canonical-model/PREDICATE_REGISTRY_v1.0.json`
5. Implementação: `current/atlas-web/`

Os ZIPs em `historical-artifacts/` são somente rastreabilidade.

## Snapshot canônico atual após MASS01 e R01

- 920 entidades e 920 Entity Pages
- 610 statements
- 165 sources
- 736 claims e 737 evidences
- 56 predicates controlados
- 398 entidades editoriais com mídia local e licenciada
- 522 entidades catalográficas; 6 com primeira verificação individual R01
- 146 entidades completas, 252 substanciais e 522 catalogadas
- 4/4 geometrias revisadas e release-ready
- SQLite SHA-256: atualizado no manifesto de release após cada expansão validada

## Gates

| Gate | Estado |
|---|---|
| SQLite, FK, UUIDv7, evidence e predicates | PASS |
| Exportação determinística | PASS |
| Astro, Pagefind, dist e links | PASS |
| Mídia editorial atual e geografia atual | PASS |
| Mídia do universo expandido | OPEN — executar Fase 10 |
| Acessibilidade, Lighthouse e percursos do baseline v1.0.0 | PASS histórico |
| Acessibilidade e Lighthouse sobre 920+ Entities | OPEN — executar Fase 12 |
| Chrome/Edge, Firefox e WebKit do baseline v1.0.0 | PASS histórico |
| Matriz multibrowser da expansão | OPEN — executar Fase 12 |
| CI e GitHub Pages | PASS |
| Heurist hands-on piloto | PASS histórico — 9/10, sem perda crítica |
| Round-trip da expansão e geometria Heurist | OPEN — executar Fase 13 |
| A9.7 Product Complete | PASS para o baseline v1.0.0 |
| Conclusão integral do escopo expandido | OPEN — seguir G0–G12 e GF |

## Heurist

A base `felip_atlas_a97` no Heurist Huma-Num 7.2.1 contém 86 Entity, 24 Source e 131 Statement importados com zero erros. O único requisito não pontuado foi o mapa interno, pois a projeção piloto não levou geometrias. O resultado completo está em `handoff/heurist-result.json`.

O A9.7 e a tag `v1.0.0` permanecem aprovados para seu baseline histórico. A expansão atual reabre gates editoriais e de QA, não a arquitetura. O plano operacional corrente é `handoff/ATLAS_COMPLETION_MASTER_PLAN.md`.
