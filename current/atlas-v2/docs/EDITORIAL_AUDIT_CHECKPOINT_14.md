# Checkpoint 14 — Auditoria editorial transversal

Data: 2026-08-24

## Objetivo

Medir os 258 capítulos com os mesmos critérios e transformar lacunas editoriais
em backlog reproduzível. Este checkpoint não declara o produto completo; ele
estabelece a linha de base para concluir conteúdo, mídia e geografia.

## Resultado

- Status estrutural: PASS.
- Capítulos: 258/258, cobrindo exatamente 1769–2026.
- Entidades publicáveis: 965; citadas pelos capítulos: 82.
- Capítulos com claim no ano exato: 125.
- Capítulos com claim no ano ou intervalo aplicável: 169.
- Gap temporal: 89 capítulos.
- Capítulos apontando para arquivo visual existente: 258; ativos únicos: 6.
- Manifesto licenciado de mídia por história: ausente; backlog: 258.
- Geometrias temporais: 1; capítulos ligados a entidade mapeada: 1.
- Inventário espacial não classificado: limite superior de 257 capítulos.

## Interpretação

O `PASS` significa que o acervo é íntegro e auditável: anos, referências,
fontes, URLs, textos mínimos e arquivos declarados não estão quebrados. Não
significa curadoria encerrada. Permanecem abertos os gates de correspondência
temporal, mídia licenciada específica e cartografia do subconjunto espacial.

## Contrato automatizado

```powershell
python scripts/audit_editorial_coverage.py
python scripts/audit_editorial_coverage.py --check
```

O primeiro comando regenera `reports/editorial-coverage.json`; o segundo exige
que o relatório versionado seja idêntico ao estado canônico. O CI executa o
segundo comando e bloqueia deriva silenciosa.

## Próximo checkpoint

O CP15 fecha os 89 gaps temporais. Sua saída obrigatória é
`chaptersWithTemporalSupport = 258` e `chaptersWithoutTemporalSupport = 0`, sem
inventar datas: cada correção exige claim e fonte recuperável ou reescrita do
capítulo para o intervalo efetivamente sustentado.
