# ATLAS — continuidade após v1.0.0

> Plano corrente: `handoff/ATLAS_COMPLETION_MASTER_PLAN.md`. Este arquivo é apenas um resumo de continuidade; contagens e checkpoints devem seguir o plano mestre e `CURRENT_STATUS.md`.

O A9.7 está concluído. A continuidade é manutenção de produto e conteúdo, sem reabrir a arquitetura static-first.

## Fluxo normal

1. Editar o SQLite canônico em `current/atlas-web/data/atlas.sqlite` por processo reproduzível.
2. Executar `npm ci` e `npm run verify` em `current/atlas-web/`.
3. Confirmar cobertura de mídia, geografia e links.
4. Fazer pull request; o GitHub Actions valida e publica o Pages a partir de `main`.

## Próximas versões

- `v1.x`: novas informações históricas, fontes, correções editoriais e qualidade.
- Alterações no modelo semântico congelado exigem change control.
- Não introduzir backend, banco paralelo, graph database ou autenticação sem novo gate arquitetural.

URL pública: <https://flpgiacomini.github.io/atlas/>
