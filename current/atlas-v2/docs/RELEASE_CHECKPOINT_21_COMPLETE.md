# CP21 — corte e lançamento do Atlas v2

Data: 2026-08-25.

## Resultado

O Atlas v2 substituiu a v1 em um corte único e encerrou o CP21 com **PASS**.

- URL pública: <https://flpgiacomini.github.io/atlas/>
- Commit do corte: `4c125ccc72bd3094965845f7a1e9e8de1b7a3c9d`
- Versão: `2.0.0`
- Tag anotada: `v2.0.0`
- CI do corte: <https://github.com/flpgiacomini/atlas/actions/runs/32888450760>
- Pages do corte: <https://github.com/flpgiacomini/atlas/actions/runs/32888450887>

## Smoke público

O Chrome carregou a página pública como “Atlas v2 — História Interativa do
Automóvel”. História, timeline, mapa MapLibre, globo Cesium e alternativa
textual foram exercitados sem erros ou avisos no console.

As rotas 1886, 1908, 1955, 1958, 1963, 1969 e 2026 retornaram HTTP 200. O bundle
`data/v2/geography.json`, `cesium/Cesium.js` e o worker
`cesium/Workers/createGeometry.js` também retornaram HTTP 200 sob `/atlas/`.

## Conteúdo da versão

- 258 capítulos anuais de 1769 a 2026.
- 966 entidades nos bundles de publicação.
- 522/522 decisões de curadoria auditadas.
- 97 geometrias temporais.
- 95/95 histórias interativas espacialmente cobertas.
- 258/258 capítulos com decisão de mídia e 38 itens licenciados.
- 53 bundles determinísticos.
- 260 páginas estáticas.

Os checksums de integridade estão em
`reports/release-v2.0.0-checksums.sha256`.

## Limitações conhecidas

- O runtime local do Cesium aumenta o artefato para aproximadamente 140 MB,
  mas permanece fora do carregamento inicial.
- A matriz bloqueante é Chrome desktop; mobile recebe uma experiência
  simplificada e alternativas textuais.
- A cobertura histórica é curada e conectada, não uma reprodução exaustiva de
  todo catálogo automotivo existente.

Checkpoint CP21: **PASS**. Atlas v2.0.0: **publicado**.
