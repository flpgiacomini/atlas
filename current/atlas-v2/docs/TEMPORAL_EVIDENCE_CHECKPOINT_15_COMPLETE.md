# CP15 — Evidência temporal concluída

Data: 2026-08-24

## Resultado final

- Capítulos anuais: 258/258.
- Claims no ano exato: 133.
- Capítulos sustentados por intervalo declarado: 44.
- Continuidade entre marcos documentados: 81.
- Suporte temporal total: 258/258.
- Gaps temporais: 0.

## Contrato editorial

Um capítulo `milestone` exige claim no ano ou intervalo aplicável. Um capítulo
`continuity` pode usar `temporalContext` para declarar uma ou mais entidades
canônicas cujos marcos envolvem o ano narrado. Quando há mais de uma entidade,
as âncoras são agregadas somente para delimitar o período.

Esse mecanismo não transforma continuidade em ocorrência anual. O relatório
preserva separadamente os 133 anos com claim exato e os 81 capítulos situados
entre marcos.

## Lotes executados

1. Oito milestones foram reassociados e reescritos para eventos datados.
2. O período 1802–1824 recebeu contexto próprio com quatro marcos documentados.
3. Os 32 gaps residuais receberam pares de entidades canônicas de curta duração,
   sempre posicionados antes e depois do ano narrado.

## Gate

O CP15 está encerrado. Qualquer alteração futura que reintroduza um gap será
visível em `reports/editorial-coverage.json` e bloqueada como regressão pelo CI.
O próximo gate é o CP16: completar narrativa, mídia, geografia e visualizações
dos seis percursos obrigatórios.
