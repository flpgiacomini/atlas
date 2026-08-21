# Atlas v2 — aplicação

Aplicação estática Astro + React da segunda geração do Atlas. Ela consome os
bundles canônicos produzidos em `../atlas-v2`, preservando a versão pública
atual até o corte editorial definitivo.

## Desenvolvimento

Requer Node.js 22.

```bash
npm ci
npm run dev
```

O comando de desenvolvimento sincroniza primeiro os bundles e ativos
editoriais. A aplicação é servida sob `/atlas/`.

## Gate local

```bash
npm run verify
```

O gate executa `astro check`, testes unitários, sincronização canônica, build
estático e validação das 258 rotas anuais, do `404` e dos ativos essenciais.

## Contratos já implementados

- rotas anuais prerenderizadas de 1769 a 2026;
- timeline global sincronizada com URL e histórico do navegador;
- busca tolerante a acentos, limitada ao conhecimento datado disponível no ano;
- carregamento progressivo e cache de bundles por período e categoria;
- seis percursos editoriais canônicos e modal em camadas;
- modos História, Mapa/Globo, Marcas, Veículos, Competições e Tecnologias;
- URLs compatíveis com GitHub Pages em `/atlas/`.

MapLibre, Cesium e as visualizações especializadas completas entram nos
checkpoints seguintes. Os controles atuais definem o contrato de estado comum
que essas projeções deverão obedecer.
