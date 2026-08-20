# ADR-001 — Autoridade documental e experiência temporal

Status: aceito  
Data: 2026-08-20

## Contexto

O Atlas v1 usa SQLite como autoridade e publica páginas e ferramentas separadas.
A v2 deve contar uma história contínua de 1769 a 2026, sincronizando capítulos,
mapa, globo, marcas, veículos, competições e tecnologias.

## Decisão

1. JSON-LD, Markdown estruturado e GeoJSON temporal substituem o SQLite.
2. IDs públicos usam o formato `atlas:<tipo>:<slug-estavel>`.
3. Astro preservará prerender e metadados; React coordenará o estado temporal.
4. A timeline é a navegação global. O ano selecionado limita o conhecimento
   apresentado por todas as visualizações.
5. Entidades abrem em modais sem URL própria.
6. MapLibre e Cesium são carregados somente em exploração espacial. Mapas que
   apenas explicam rota, caminho ou mudança podem ser imagens editoriais.
7. Grafo genérico, comparação e páginas públicas de entidade não seguem para v2.
8. A v2 é construída em paralelo; o corte ocorre somente após todos os gates.

## Consequências

- URLs v1 serão encerradas no corte.
- A migração precisa emitir uma tabela completa de identidade antiga/nova.
- Cada afirmação pública precisa apontar para pelo menos uma fonte confiável.
- Toda história espacial precisa apontar para geometria temporal validada.
- A interface deve carregar dados e motores cartográficos progressivamente.
