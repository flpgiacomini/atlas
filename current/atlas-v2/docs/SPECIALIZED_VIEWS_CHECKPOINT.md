# Checkpoint — visualizações especializadas

Data: 2026-08-21

## Implementado

- Marcas: rio regional que separa registros datados do catálogo ainda sem
  cronologia corporativa.
- Veículos: linhagem temporal dos marcos documentados até o ano global.
- Competições: quadro de temporada com provas recuperadas no período e séries
  catalogadas.
- Tecnologias: fluxo temporal de tecnologias datadas e eventos cujo próprio
  título explicita o marco técnico.
- Geografia: prévia editorial que declara explicitamente que ainda não é a
  cartografia MapLibre/Cesium definitiva.
- Todas as projeções possuem resumo textual acessível e estados vazios honestos.

## Cobertura canônica observada

| Categoria | Total | Com início datado |
|---|---:|---:|
| Marcas | 504 | 1 |
| Veículos | 142 | 55 |
| Séries | 4 | 0 |
| Tecnologias | 37 | 2 |

O produto não infere datas ausentes. As visualizações tornam o débito editorial
visível e mensurável, preservando a distinção entre catálogo e história
temporalmente comprovada.

## QA Chrome desktop

- quatro projeções especializadas carregadas e sincronizadas em 1969;
- navegação principal permaneceu funcional;
- nenhum erro ou aviso no console;
- fallback textual presente em todos os modos.

## Próximo gate

Elevar a cobertura temporal dos registros de marca e série antes de representar
fusões, aquisições, renomes, temporadas e genealogias como relações. Depois,
implementar GeoJSON temporal, MapLibre e Cesium.
