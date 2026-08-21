# Registry temporal de marcas — lote 02

Data: 2026-08-21

## Cobertura acumulada

- 19 marcas;
- 22 marcos temporais;
- 922 entidades no universo v2;
- 41 bundles determinísticos.

## Marcas acrescentadas

Peugeot, Opel, Cadillac, Buick, Rolls-Royce, Alfa Romeo, BMW, Volvo,
Volkswagen, Toyota, Ferrari e Porsche.

## Correção canônica

Porsche não existia como entidade `Brand` na migração, apesar de constituir um
dos seis percursos obrigatórios. Foi criada a entidade semântica
`atlas:brand:porsche`, distinta da empresa de engenharia de 1931, e sua origem
automotiva foi ligada ao registro do 356 No. 1 em 8 de junho de 1948.

## Decisões de modelagem

- Peugeot é datada pelo primeiro modelo automotivo da marca em 1889, não pela
  origem industrial familiar de 1810.
- Opel é datada pelo início oficial da produção automobilística em 1899.
- Cadillac, Buick, BMW, Volkswagen e Toyota possuem marcos de operadora quando
  a fonte descreve constituição empresarial.
- Toyota possui separadamente o estabelecimento do logotipo em 1936 e da
  companhia em 1937.
- Rolls-Royce é datada pelo acordo de 1904 para comercializar automóveis sob o
  nome conjunto.
- Ferrari é datada pelo primeiro funcionamento da 125 S em 1947.

## Fontes

Foram usadas exclusivamente páginas institucionais de Peugeot/Stellantis,
Opel/Stellantis, General Motors, Rolls-Royce Motor Cars, Alfa Romeo/Stellantis,
BMW Group, Volvo Cars, Volkswagen Group, Toyota Motor Corporation, Ferrari e
Porsche AG. Fontes novas registram a data de verificação; referências já
migradas preservam seu próprio registro canônico de verificação.

## Próximo lote

Adicionar relações binárias temporais entre marcas e organizações. O contrato
seguinte deverá exigir `from`, `to`, tipo controlado, fonte, confiança e notas
de continuidade para fusões, aquisições, renomes, sucessões e renascimentos.
