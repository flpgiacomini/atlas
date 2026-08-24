# CP17 — inventário e cobertura cartográfica completos

Data de verificação: 2026-08-24

## Resultado final

O CP17 está **concluído**. Todos os 258 capítulos foram classificados e todas
as histórias que exigem interação possuem ao menos uma geometria com validade
no ano correspondente:

- **95/95** capítulos `interactive-required` cobertos;
- **163** capítulos `static-sufficient` com decisão editorial explícita;
- **0** capítulos não classificados;
- **0** pendências interativas;
- **97** features temporais em **32** coleções GeoJSON.

## Refinamento do inventário

A classificação inicial apontava 98 capítulos interativos. A revisão de fontes
reclassificou 1950, 1956 e 1960 como `static-sufficient`: são capítulos de
transição, e seus acontecimentos espaciais documentados começam apenas no ano
seguinte. A decisão evita estender geometrias retroativamente.

## Lote 2000–2026

O lote final incorporou 25 anos, cobrindo expansão do Prius, iDrive, rede
produtiva do Cayenne, Panda, Veyron, estratégia da Tesla, ESC, crise de 2008,
Leaf, BMW i, Model S, MQB, Dieselgate, Bolt, Model 3, ID.3, pandemia, políticas
de comércio elétrico e mercados globais de 2025–2026.

As últimas lacunas materiais — Nürburgring em 1930–1931, Traction Avant em 1934
e Toyoda Model AA em 1936 — também foram fechadas.

## Gate bloqueante

O CI falha quando:

- um dos 258 capítulos não está classificado exatamente uma vez;
- um capítulo interativo não tem geometria válida no próprio ano;
- a feature não registra fonte, precisão, confiança e validade;
- o intervalo temporal está invertido;
- o ID de geometria é duplicado;
- a geometria GeoJSON é vazia ou usa tipo não aceito;
- o relatório versionado está desatualizado.

## Limitações conhecidas

- linhas editoriais não são reconstruções de itinerário;
- âncoras nacionais e regionais não substituem fronteiras históricas detalhadas;
- cobertura mínima da entidade principal não significa que todos os lugares de
  um capítulo multientidade já possuam relações próprias;
- mapas estáticos e mídia geográfica serão tratados no CP18.

## Próximo checkpoint

O caminho crítico avança para o **CP18 — mídia editorial por história**:
manifesto, arquivo local, licença, crédito, texto alternativo e decisão de
apresentação para os 258 capítulos.
