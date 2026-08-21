# Checkpoint — núcleo da aplicação v2

Data: 2026-08-21

## Escopo concluído

- Astro static-first com React como camada integral de interação.
- 258 rotas anuais (`1769`–`2026`), índice e página `404`.
- Estado temporal global refletido na URL, `pushState`, voltar e avançar.
- Timeline por arraste, clique e teclado, sem reprodução automática.
- Busca normalizada para acentos e limitada a registros com horizonte temporal
  verificável no ano selecionado.
- Bundles canônicos carregados sob demanda e mantidos em cache por sessão.
- Modal editorial com narrativa, cronologia, relações e fontes.
- Seis modos de visualização conectados ao mesmo ano global.
- Build compatível com `base=/atlas`.

## Evidência automática

- `astro check`: 0 erros, 0 avisos e 0 sugestões.
- testes unitários: 4/4 aprovados.
- build: 260 páginas estáticas.
- validador de distribuição: 258/258 anos e ativos essenciais presentes.

## Evidência no Chrome desktop

- rota inicial `/atlas/1969/` carregada com 921 entidades canônicas;
- clique, teclado e histórico do navegador revalidados;
- busca por `Prius` ocultada em 1969 e disponível em 1997;
- modal editorial e modo Marcas carregados;
- nenhuma mensagem de erro ou aviso no console.

## Próximo checkpoint

Implementar as projeções especializadas reais: rio genealógico de marcas,
linhagens de veículos, temporadas, agenda e fluxos tecnológicos. Em seguida,
integrar MapLibre e Cesium com GeoJSON temporal.
