# ATLAS — estado atual

**Data:** 25/08/2026  
**Fase:** Atlas v2.0.0 publicado; manutenção editorial contínua  
**Aplicação vigente:** `current/atlas-v2-app/`  
**Autoridade canônica:** `current/atlas-v2/`  
**URL:** <https://flpgiacomini.github.io/atlas/>

## Source of truth

1. Conteúdo: `current/atlas-v2/content/`
2. Schemas: `current/atlas-v2/schemas/`
3. Bundles: `current/atlas-v2/bundles/`
4. Aplicação: `current/atlas-v2-app/`
5. Estado detalhado: `current/atlas-v2/docs/IMPLEMENTATION_PANORAMA.md`

O SQLite e `current/atlas-web/` são legado rastreável da v1 e não participam
do build público. Os ZIPs em `historical-artifacts/` continuam sendo somente
rastreabilidade.

## Snapshot v2.0.0

- 258 capítulos anuais, de 1769 a 2026
- 966 entidades projetadas em 53 bundles determinísticos
- 920 entidades migradas da v1 sem perda silenciosa
- 522/522 decisões de curadoria auditadas
- 97 geometrias temporais e 95/95 histórias interativas cobertas
- 258/258 capítulos com decisão de mídia; 38 itens licenciados
- seis percursos editoriais obrigatórios conectados
- 260 páginas estáticas publicadas sob `/atlas/`

## Gates

| Gate | Estado |
|---|---|
| Contratos, referências e round-trip | PASS |
| Migração e bundles determinísticos | PASS |
| 258 capítulos e evidência temporal | PASS |
| C18 — 522 decisões semânticas | PASS |
| Mídia e cartografia temporal | PASS |
| Seis percursos editoriais | PASS |
| Astro, testes e build `/atlas/` | PASS |
| Chrome desktop e smoke mobile | PASS |
| CI e GitHub Pages | PASS |
| CP20 — QA candidato | PASS |
| CP21 — corte v2.0.0 | PASS |

Relatório de release:
`current/atlas-v2/docs/RELEASE_CHECKPOINT_21_COMPLETE.md`.
