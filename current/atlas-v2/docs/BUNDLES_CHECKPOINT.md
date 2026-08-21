# Checkpoint — Bundles e seis percursos conectados

Data: 2026-08-21  
Estado: implementação validada localmente

## Resultado

- 921 entidades no índice de publicação: 920 migradas e um evento editorial
  indispensável de 1955.
- 40 bundles segmentados por categoria, período e região.
- Dez recortes temporais publicados, incluindo `undated` como dívida explícita.
- Seis percursos obrigatórios conectados a documentos canônicos.
- Manifesto registra contagem, caminho e SHA-256 de cada bundle.
- Protótipo carrega `journeys.json` em runtime e deixou de manter os seis
  registros duplicados no componente React.
- Modal apresenta narrativa, cronologia, relações e fontes recuperadas do
  bundle.
- Estados de carregamento, erro e cobertura são explícitos.

## Cobertura temporal observada

732 entidades ainda estão no bundle `undated`. Isso não representa perda de
dados: identifica registros cuja migração não fornece data suficiente para
segmentação histórica. A expansão editorial deverá reduzir esse número sem
inferir datas automaticamente.

## Evento editorial de 1955

O percurso de 1955 recebeu uma entidade v2 própria, sustentada por fontes
institucionais da DS Automobiles/Stellantis e Mercedes-Benz Media. Ela conecta
a estreia do DS 19 em Paris à reflexão sobre inovação, competição e segurança
provocada pela temporada de 1955.

## Reprodução

```powershell
cd current/atlas-v2
python scripts/build_bundles.py
python scripts/validate_bundles.py
python scripts/check_bundles_determinism.py

cd ../atlas-v2-prototype
npm run build
npm run test:sites
```

## Próximo gate

Implementar o núcleo da SPA definitiva em Astro + React, incluindo estado
temporal compartilhado, rotas anuais, cache dos bundles e central de busca.
As visualizações MapLibre e Cesium continuam progressivas e entram depois que
esse núcleo consumir os contratos canônicos sem dados demonstrativos.
