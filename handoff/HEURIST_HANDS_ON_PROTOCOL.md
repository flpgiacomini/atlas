# Gate hands-on Heurist — protocolo A9.7

Estado: **APROVADO em 18/08/2026 — 9/10, sem perda semântica crítica**. Credenciais, tokens, cookies e exports privados nunca são gravados no repositório.

## Pilotos

Executar os cinco pilotos definidos no handoff, incluindo obrigatoriamente Porsche 917, Porsche 911 e seus registros de Entry/evidence. Cada piloto deve completar importação, edição controlada, exportação e comparação semântica com o SQLite canônico.

## Matriz de aprovação (10 pontos)

Marcar 1 ponto para cada requisito demonstrado:

1. Entity preservada com UUID e tipo.
2. Relação temporal preservada.
3. Conflito 901 → 911 representado sem perda.
4. Source e evidence vinculados ao claim correto.
5. Entry do Porsche 917 preservada.
6. Genealogia navegável.
7. Filtros úteis e reproduzíveis.
8. Mapa com geometrias controladas.
9. Rede com predicates preservados.
10. Round-trip sem perda semântica crítica.

## Evidências a registrar

- versão e URL da instância Heurist;
- data, executor e duração;
- IDs dos cinco pilotos;
- capturas de tela ou relatório exportado sem segredos;
- diff semântico antes/depois;
- pontuação total e perdas encontradas;
- decisão `APROVADO` (mínimo 8/10, sem perda crítica) ou `REPROVADO`.

## Ciclo de integração

Demonstrar e registrar: `Zotero/OpenRefine/Heurist → SQLite → validação → exportação → Astro → Pagefind → página publicada`.

Uma reprovação produz relatório objetivo e mantém o A9.7 aberto; não autoriza substituição silenciosa de ferramenta.

## Resultado executado

- Entity, relações temporais, conflito 901→911, source/evidence, Entry 917, genealogia, filtros, rede e round-trip: aprovados.
- Mapa interno do Heurist: não pontuado, pois o piloto não importou geometrias; a projeção pública mantém 4/4 geometrias release-ready.
- Imports: 86 Entity, 24 Source e 131 Statement; 241 registros processados, zero erros.
- Resultado consolidado: `handoff/heurist-result.json`.
