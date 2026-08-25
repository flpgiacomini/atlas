# ATLAS — história automotiva em rede

Este é o workspace mestre do Atlas: um atlas global, histórico e explorável da
indústria automobilística, centrado nos veículos e sustentado por relações,
eventos, fontes e evidências.

Site: <https://flpgiacomini.github.io/atlas/>

## Desenvolvimento

O produto vigente está em `current/atlas-v2-app/`, alimentado pela autoridade
documental em `current/atlas-v2/`. Para validar localmente:

```powershell
cd current/atlas-v2-app
npm ci
npm run verify
```

## Comece por aqui

1. `handoff/ATLAS_MASTER_HANDOFF.md` — histórico e especificação consolidada.
2. `handoff/CURRENT_STATUS.md` — o que é Source of Truth hoje.
3. `handoff/CONTINUE_FROM_HERE.md` — próximas tarefas na ordem recomendada.
4. `handoff/DECISION_REGISTER.md` — decisões que não devem ser reabertas casualmente.
5. `current/atlas-v2-app/` — **aplicação pública vigente**.
6. `current/atlas-v2/` — **conteúdo canônico, schemas, bundles e relatórios**.
6. `manifests/ALL_GENERATED_FILES.csv` — inventário de todos os arquivos gerados nos artefatos anteriores.

## Regra principal

**Não desenvolva a partir de `historical-artifacts/`.**

Esses arquivos existem apenas para rastreabilidade.

O desenvolvimento atual começa em:

```text
current/atlas-v2-app/
```

Autoridade canônica:

```text
current/atlas-v2/content/
```

Snapshot da publicação v2:
- 966 entidades projetadas
- 258 capítulos anuais, de 1769 a 2026
- 97 geometrias temporais
- 38 itens de mídia editorial licenciada
- 53 bundles determinísticos

Fase:
**Atlas v2.0 — candidato aprovado no CP20 e publicado pelo CP21.**
