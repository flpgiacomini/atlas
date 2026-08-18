# ATLAS — estado atual

**Data:** 18/08/2026

**Fase:** A9.7 Product Complete — **APROVADA**

**Implementação vigente:** `current/atlas-web/`
**URL:** <https://flpgiacomini.github.io/atlas/>

## Source of truth

1. Escopo: `current/project-spec/ATLAS_SCOPE_FREEZE_v1.0.md`
2. Modelo: `current/canonical-model/docs/ATLAS_CANONICAL_DATA_MODEL_v1.0.md`
3. SQLite: `current/atlas-web/data/atlas.sqlite`
4. Predicate Registry: `current/canonical-model/PREDICATE_REGISTRY_v1.0.json`
5. Implementação: `current/atlas-web/`

Os ZIPs em `historical-artifacts/` são somente rastreabilidade.

## Snapshot aprovado

- 339 entidades e 339 Entity Pages
- 446 statements
- 125 sources
- 572 claims/evidences
- 54 predicates controlados
- 339/339 entidades com mídia local e licenciada
- 4/4 geometrias revisadas e release-ready
- SQLite SHA-256: `62392b653dec0c1ba490ebcd4fd13e7bb2cde0e5b8cdb21fafe79f01c5afa33d`

## Gates

| Gate | Estado |
|---|---|
| SQLite, FK, UUIDv7, evidence e predicates | PASS |
| Exportação determinística | PASS |
| Astro, Pagefind, dist e links | PASS |
| Mídia e geografia | PASS |
| Acessibilidade, Lighthouse e percursos visuais | PASS |
| Chrome/Edge, Firefox e WebKit | PASS |
| CI e GitHub Pages | PASS |
| Heurist hands-on | PASS — 9/10, sem perda crítica |
| A9.7 Product Complete | PASS |

## Heurist

A base `felip_atlas_a97` no Heurist Huma-Num 7.2.1 contém 86 Entity, 24 Source e 131 Statement importados com zero erros. O único requisito não pontuado foi o mapa interno, pois a projeção piloto não levou geometrias. O resultado completo está em `handoff/heurist-result.json`.

Não existem hard gates abertos. Após a tag `v1.0.0`, o trabalho passa a ser conteúdo, correções e qualidade em `v1.x`.
