# Relatório A9.7 — candidato a release

Data da revisão: 2026-08-18  
Estado: **APROVADO — A9.7 Product Complete; candidato v1.0.0**

## Identificação

- Produto: Atlas — arquivo editorial histórico em português
- Site previsto: <https://flpgiacomini.github.io/atlas/>
- Banco canônico: `current/atlas-web/data/atlas.sqlite`
- SHA-256 do banco: `62392B653DEC0C1BA490EBCD4FD13E7BB2CDE0E5B8CDB21FAFE79F01C5AFA33D`
- Baseline Git: `34b41d7c9ca47badfb5b875af7aff3f611b1f786`
- Candidato implantado: `a1cdbd14e8254d74f86925f0eca96c50e4a1b490`
- URL pública: <https://flpgiacomini.github.io/atlas/>
- Ambiente local de validação: Node 26.7.0, npm 11.19.0 e Python 3.14.7
- Ambiente CI contratado: Node 22 e Python 3.13

## Resultados aprovados

| Gate | Resultado |
|---|---:|
| Entidades / páginas de entidade | 339 / 339 |
| Statements | 446 |
| Sources | 125 |
| Claims/evidence | 572 |
| Predicates controlados | 54 |
| Integridade SQLite, FK e contrato semântico | aprovado |
| Exportação determinística | aprovado |
| Manifesto e cobertura de mídia | 339 / 339 |
| Ilustrações editoriais locais | 5 WebP, 2.267.430 bytes |
| Geografias revisadas e release-ready | 4 / 4 |
| Testes unitários | 4 / 4 |
| Astro check | 0 erros, 0 avisos |
| HTML validado | 345 páginas |
| Auditoria de links | 345 páginas, aprovada |
| Pagefind | 339 páginas pt-BR, 2.979 palavras |
| Artefato `dist` | 727 arquivos, 8.262.622 bytes |
| Lighthouse | performance 94, acessibilidade 100, boas práticas 100, SEO 100 |
| Chrome/Edge | percursos obrigatórios aprovados |
| Firefox | smoke test aprovado |
| WebKit | smoke test aprovado |
| GitHub Actions CI | aprovado, execução nº 4 |
| GitHub Pages | aprovado, workflow nº 5 |
| Smoke test público | home, Pagefind, sitemap e Entity Page com HTTP 200 |
| Heurist hands-on | 9/10, 86 Entity + 24 Source + 131 Statement, 0 erros |

O erro final do Lighthouse foi restrito à remoção de seu diretório temporário no Windows e ocorreu depois da emissão válida do relatório.

## Validação editorial e funcional

Foram inspecionados os percursos Porsche 917, Porsche 911, Benz Patent Motor Car, Ford Model T, origens do Motorsport e Volvo PV544. Busca, comparação, mapa, timeline, grafo e navegação sob `/atlas/` foram exercitados. O caminho textual Porsche 917 → 1970 Le Mans Entry → Richard Attwood foi confirmado.

## Gate Heurist

O hands-on foi aprovado em 18/08/2026 com 9/10 e sem perda semântica crítica. A base `felip_atlas_a97` importou 86 entidades, 24 fontes e 131 statements, todos processados sem erro. Relações temporais, conflito 901→911, Entry do 917, genealogia, evidence, filtros, rede e round-trip foram confirmados. O mapa interno não pontuou porque a projeção piloto não incluiu geometrias; o mapa público permanece aprovado com 4/4 geometrias controladas.

Não restam pendências impeditivas. O commit e a tag definitivos serão registrados após a última validação e publicação.

## Limitações conhecidas

- As imagens editoriais são ilustrações originais, identificadas como interpretativas; não são documentos históricos.
- Os bundles de visualização são locais e aumentam o JavaScript inicial em páginas específicas.
- O GitHub Pages não permite configurar headers HTTP personalizados; os controles compatíveis foram implementados por metadados e arquivos estáticos.
