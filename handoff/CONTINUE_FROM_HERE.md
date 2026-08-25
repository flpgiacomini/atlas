# ATLAS — continuidade após v2.0.0

O ciclo de lançamento da v2 está concluído. A continuidade é manutenção e
expansão editorial sem reabrir silenciosamente os contratos aprovados.

## Fluxo normal

1. Alterar documentos em `current/atlas-v2/content/` com fonte e evidência.
2. Regenerar e validar migração/bundles pelos scripts de `current/atlas-v2/`.
3. Executar `npm ci` e `npm run verify` em `current/atlas-v2-app/`.
4. Revisar mídia, geografia, narrativa e comportamento temporal afetados.
5. Enviar ao `main`; CI valida e Pages publica automaticamente.

## Regras preservadas

- Não recolocar SQLite no build público.
- Não inferir geografia ou fatos em runtime.
- Não publicar afirmações ou mídia sem fonte/licença.
- Preservar conflitos documentais como conflitos.
- Mudanças incompatíveis nos schemas exigem ADR e nova versão principal.

URL pública: <https://flpgiacomini.github.io/atlas/>
