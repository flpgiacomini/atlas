# CP17 — inventário cartográfico dos 258 capítulos

Data de verificação: 2026-08-24

## Objetivo

Transformar a cartografia de uma expectativa genérica em um contrato editorial
mensurável. Cada capítulo de 1769 a 2026 recebe exatamente um modo espacial:

- `interactive-required`: lugar, rota, circuito ou relação geográfica é parte
  indispensável da história e exige GeoJSON temporal;
- `static-sufficient`: um mapa editorial estático ou cartão contextual conta a
  dimensão espacial sem impor interação desnecessária;
- `not-spatial`: a geografia não acrescenta compreensão material e sua ausência
  precisa ser uma decisão explícita.

## Regras da primeira classificação

Os seis percursos, capítulos já dirigidos por geografia, competições e relações
entre múltiplos lugares são interativos obrigatórios. Escalas regionais ou
globais e capítulos centrados em um único contexto podem usar representação
estática. A classificação é determinística e será refinada por decisão
editorial documentada, não por geocodificação em runtime.

## Gates

- 258/258 capítulos classificados uma única vez;
- todo GeoJSON com validade, precisão, confiança e fonte;
- estado de cobertura regenerado a partir dos documentos canônicos;
- relatório versionado e verificado no CI;
- nenhuma geometria inferida durante a navegação.

O inventário canônico está em `content/spatial-inventory.json`; o resultado
auditável está em `reports/spatial-coverage.json`.

## Próximo lote

Priorizar os anos `interactive-required` sem geometria, em ordem cronológica e
por conjuntos narrativos reutilizáveis. Cada lote deverá resolver fonte e
precisão antes de publicar coordenadas, começando pelos capítulos anteriores a
1886 e pelas primeiras rotas públicas.
