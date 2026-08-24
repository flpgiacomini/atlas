# CP16 — progresso 01 dos seis percursos

Data de verificação: 2026-08-24

## Resultado

O percurso **Porsche 917 / 1969** é o primeiro pacote editorial completo do
checkpoint CP16. Ele estabelece o contrato de referência para os cinco
percursos restantes, mas **não encerra o CP16**.

| Percurso | Evidência canônica | Narrativa completa | Mídia licenciada | Geometria temporal | Ativo de apresentação |
| --- | --- | --- | --- | --- | --- |
| Porsche 917 / 1969 | sim | sim | sim | sim | sim |
| Porsche 911 / 1963 | sim | não | não | não | sim |
| Volvo PV544 / 1958 | sim | não | não | não | sim |
| Origens do Motorsport / 1955 | sim | não | não | não | sim |
| Ford Model T / 1908 | sim | não | não | não | sim |
| Benz Patent-Motorwagen / 1886 | sim | não | não | não | sim |

## Pacote de referência do Porsche 917

- capítulo anual com quatro `StoryBeat` e citações recuperáveis;
- quatro claims datados: conclusão, apresentação, homologação e primeira vitória;
- fontes e evidências ligadas a cada afirmação;
- imagem editorial e mapa ilustrativo locais, com autoria, licença, crédito e
  texto alternativo no manifesto de mídia;
- rota aproximada com validade temporal, precisão, confiança e fonte;
- modal capaz de apresentar mídia e distinguir material histórico de
  ilustração editorial;
- bundle segmentado e geração determinística.

## Métricas do checkpoint

- percursos catalogados: **6/6**;
- percursos com evidência canônica: **6/6**;
- percursos editorialmente completos: **1/6**;
- percursos com mídia licenciada: **1/6**;
- percursos com geografia temporal: **1/6**;
- ativos temáticos de apresentação: **6/6**;
- cobertura temporal do Atlas: **258/258 anos**, sem gaps estruturais;
- cobertura de mídia histórica/editorial específica: **1/258 capítulos**.

## Gate e próximos lotes

O auditor `audit_journey_coverage.py` bloqueia regressões no inventário,
referências, arquivos, licenças, evidência, histórias completas e geografia.
Seu `PASS` significa que o estado declarado é íntegro; a conclusão do CP16
continua condicionada a `completeJourneys = 6`.

Ordem proposta para completar o checkpoint:

1. Porsche 911 / 1963;
2. Benz Patent-Motorwagen / 1886;
3. Ford Model T / 1908;
4. Volvo PV544 / 1958;
5. Origens do Motorsport / 1955.

Cada lote deve reproduzir o pacote de referência antes de ser considerado
concluído: narrativa, claims, fontes, evidências, mídia, geometria e validação
visual no modo especializado correspondente.
