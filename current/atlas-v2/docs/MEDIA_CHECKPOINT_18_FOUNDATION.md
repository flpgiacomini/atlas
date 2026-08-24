# CP18 — Fundação da mídia editorial

## Resultado

O Atlas possui agora uma decisão de apresentação explícita e validável para
cada capítulo anual. A fundação não declara cobertura visual inexistente: os
seis capítulos dos percursos obrigatórios têm mídia específica e os outros 252
permanecem como composições textuais em revisão.

## Contratos e gates

- `content/media-manifest.json` continua sendo a autoridade para arquivos,
  autoria, origem, licença, crédito, texto alternativo e natureza documental;
- `content/story-media-decisions.json` relaciona os 258 anos ao modo editorial
  e, quando aplicável, aos IDs do manifesto;
- `scripts/build_story_media_inventory.py` reproduz a linha de base;
- `scripts/audit_story_media.py` valida os dois registros e produz
  `reports/story-media-coverage.json`;
- o CI falha para ano sem decisão, arquivo local ausente, hotlink, referência
  quebrada, licença fora da política, crédito ou alt incompletos;
- os bundles anuais passam a entregar `mediaDecision` e `media`, fazendo a aba
  Mídia do modal funcionar também para o capítulo anual, não apenas no bundle
  dos seis percursos.

## Linha de base

- capítulos com decisão: **258/258**;
- capítulos com mídia específica: **6/258**;
- capítulos temporariamente textuais: **252/258**;
- itens licenciados no manifesto: **7**;
- hotlinks: **0**.

## Próximos lotes

1. **V01 — 1769–1885:** precursores, vapor, eletricidade e combustão inicial;
2. **V02 — 1886–1918:** formação do automóvel, indústria e competição;
3. **V03 — 1919–1945:** produção em massa, design, crise e guerra;
4. **V04 — 1946–1973:** reconstrução, mobilidade popular e performance;
5. **V05 — 1974–1999:** energia, segurança, eletrônica e globalização;
6. **V06 — 2000–2026:** híbridos, software, eletrificação e transição.

Cada lote deve preferir documento histórico licenciado quando ele acrescentar
evidência; usar ilustração ou mapa original claramente identificado quando a
função for interpretar; e manter composição textual quando uma imagem seria
decorativa, enganosa ou juridicamente insegura.
