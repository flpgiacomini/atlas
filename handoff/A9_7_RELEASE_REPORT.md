# Relatório A9.7 — candidato a release

Data da revisão: 2026-08-18  
Estado: **aprovado localmente; bloqueado para v1.0.0 pelo gate Heurist e pela confirmação do deploy**

## Identificação

- Produto: Atlas — arquivo editorial histórico em português
- Site previsto: <https://flpgiacomini.github.io/atlas/>
- Banco canônico: `current/atlas-web/data/atlas.sqlite`
- SHA-256 do banco: `62392B653DEC0C1BA490EBCD4FD13E7BB2CDE0E5B8CDB21FAFE79F01C5AFA33D`
- Baseline Git: `34b41d7c9ca47badfb5b875af7aff3f611b1f786`
- Candidato publicado: `23eb631` em `origin/main`
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
| GitHub Actions CI | aprovado, execução nº 2 |

O erro final do Lighthouse foi restrito à remoção de seu diretório temporário no Windows e ocorreu depois da emissão válida do relatório.

## Validação editorial e funcional

Foram inspecionados os percursos Porsche 917, Porsche 911, Benz Patent Motor Car, Ford Model T, origens do Motorsport e Volvo PV544. Busca, comparação, mapa, timeline, grafo e navegação sob `/atlas/` foram exercitados. O caminho textual Porsche 917 → 1970 Le Mans Entry → Richard Attwood foi confirmado.

## Pendências impeditivas

1. **Heurist hands-on:** aguardando credenciais temporárias fornecidas por canal seguro. O protocolo está em `HEURIST_HANDS_ON_PROTOCOL.md`. Resultado inferior a 8/10 ou perda semântica crítica mantém o release bloqueado.
2. **GitHub Pages:** build, validadores e auditoria de links passaram no workflow nº 2. A ativação foi recusada pela API com `422: Your current plan does not support GitHub Pages for this repository`, pois o repositório está privado no plano atual. É necessária decisão do proprietário entre tornar o repositório público ou alterar o plano GitHub; depois disso, o workflow e o smoke test público devem ser repetidos.

Nenhuma tag `v1.0.0` nem GitHub Release deve ser criada antes de ambos os itens serem aprovados. O commit publicado e o resultado do deploy serão acrescentados a este relatório na promoção do candidato.

## Limitações conhecidas

- As imagens editoriais são ilustrações originais, identificadas como interpretativas; não são documentos históricos.
- Os bundles de visualização são locais e aumentam o JavaScript inicial em páginas específicas.
- O GitHub Pages não permite configurar headers HTTP personalizados; os controles compatíveis foram implementados por metadados e arquivos estáticos.
