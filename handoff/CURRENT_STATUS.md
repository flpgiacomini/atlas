# ATLAS — Estado Atual

**Data do handoff:** 18/08/2026  
**Fase:** A9 — Atlas v1.0 / Product Complete  
**Pacote de código vigente:** `atlas_a9_product_v0_3.zip`  
**Banco vigente:** `current/atlas-web/data/atlas.sqlite`

## Source of Truth

Ordem de autoridade para continuação:

1. **Escopo:** `current/project-spec/ATLAS_SCOPE_FREEZE_v1.0.md`
2. **Modelo semântico:** `current/canonical-model/docs/ATLAS_CANONICAL_DATA_MODEL_v1.0.md`
3. **Schema físico:** `current/canonical-model/sql/atlas_v1_schema.sql`
4. **Predicate Registry:** `current/canonical-model/PREDICATE_REGISTRY_v1.0.json`
5. **Conteúdo atual:** `current/atlas-web/data/atlas.sqlite`
6. **Arquitetura web:** `current/architecture-reference/a8/docs/A8_ARCHITECTURE_DECISION_v1.0.md`
7. **Implementação vigente:** `current/atlas-web/`
8. **Status A9:** `current/architecture-reference/a9/docs/A9_GATE_STATUS.json`

Os ZIPs em `historical-artifacts/` são somente rastreabilidade.

## Snapshot canônico atual

- Entities: **339**
- Statements: **446**
- Sources: **125**
- Claims: **572**
- Evidences: **572**
- Predicates: **54**
- Entity names adicionais: **14**
- External identifiers: **2**
- Publishers distintos registrados: **39**
- SQLite SHA-256: `62392b653dec0c1ba490ebcd4fd13e7bb2cde0e5b8cdb21fafe79f01c5afa33d`

## Status por fase

| Fase | Estado | Observação |
|---|---|---|
| A0 Scope Freeze | CONCLUÍDA | Escopo v1 congelado |
| A1 Tool Bake-Off | CONCLUÍDO no nível de pesquisa | Heurist escolhido provisoriamente; hands-on ainda é gate do workspace |
| A2 Canonical Data Model | CONCLUÍDA | UUIDv7, SQLite, Predicate Registry, provenance |
| A3 Research Workspace | PREPARADO | Heurist/Zotero/OpenRefine configurados em blueprint; UI real ainda não validada |
| A4 Seed Diversity Test | CONCLUÍDA | 13/13 P0 passaram sem novo tipo raiz/predicate |
| A5 Chapter I 1885–1918 | CONCLUÍDA | Completo para escopo v1 |
| A6 Functional MVP | CONCLUÍDO tecnicamente | FastAPI/HTML foi protótipo; visual hands-on ficou limitado |
| A7 Content MVP | CONCLUÍDA | Cobertura global/temporal representativa |
| A8 Architecture Gate | CONCLUÍDA | Static-first/backendless decidido |
| A9 Product v1 | EM ANDAMENTO | Base Astro, UX, exploração e CI preparados; hard gates abaixo |

## Hard gates ainda abertos do A9

1. Executar `npm install` em um ambiente conectado e gerar `package-lock.json`.
2. Trocar CI para `npm ci` depois de commitar o lockfile.
3. Executar `npm run build` com Astro + Pagefind.
4. Executar `python scripts/validate_dist.py` e obter PASS.
5. Reconciliar geometrias reais e marcar pontos `release_ready`.
6. Fazer validação visual/usabilidade em navegador normal.
7. Validar na prática o fluxo Zotero/OpenRefine/Heurist ou escolher formalmente o fallback.
8. Fazer um deploy real (Cloudflare Pages primário ou fallback).
9. Realizar sessões reais de exploração e fechar A9.7.

## Itens explicitamente supersededos

- `atlas_pilot_nurburgring_v0_1`: IDs duplicados corrigidos no v0.2.
- IDs legíveis tipo `veh_000001`: migrados para UUIDv7.
- bancos `atlas_pilot_canonical_v0_3.sqlite`, A4/A5/A6/A7: snapshots históricos.
- FastAPI do A6: protótipo descartável, não backend final.
- site gerado manualmente do A8: prova arquitetural, substituído pelo scaffold Astro.
- `map-points.prototype.json`: somente desenvolvimento; não release-ready.
- A9 foundation/v0.2: substituídos pelo A9 v0.3.

