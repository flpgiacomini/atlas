# ATLAS — Master Workspace

Este é o pacote único para continuar o desenvolvimento do Atlas.

## Comece por aqui

1. `handoff/ATLAS_MASTER_HANDOFF.md` — histórico e especificação consolidada.
2. `handoff/CURRENT_STATUS.md` — o que é Source of Truth hoje.
3. `handoff/CONTINUE_FROM_HERE.md` — próximas tarefas na ordem recomendada.
4. `handoff/DECISION_REGISTER.md` — decisões que não devem ser reabertas casualmente.
5. `current/atlas-web/` — **código vigente**.
6. `manifests/ALL_GENERATED_FILES.csv` — inventário de todos os arquivos gerados nos artefatos anteriores.

## Regra principal

**Não desenvolva a partir de `historical-artifacts/`.**

Esses arquivos existem apenas para rastreabilidade.

O desenvolvimento atual começa em:

```text
current/atlas-web/
```

Banco canônico:

```text
current/atlas-web/data/atlas.sqlite
```

Snapshot atual:
- 339 Entities
- 446 Statements
- 125 Sources
- 572 Claims
- 572 Evidences
- 54 Predicates

Fase:
**A9 — Product v1.0 em andamento.**
