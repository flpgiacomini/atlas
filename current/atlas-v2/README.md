# Atlas v2 — autoridade canônica

Este diretório contém a autoridade documental do Atlas v2. A aplicação pública
é construída por `current/atlas-v2-app` e publicada pelo workflow de Pages.

O estado de cada fase, seus passos e checkpoints estão consolidados em
[`docs/IMPLEMENTATION_PANORAMA.md`](docs/IMPLEMENTATION_PANORAMA.md).

## Autoridade canônica

- `content/entities/*.jsonld`: entidades, claims, fontes e evidências.
- `content/stories/*.md`: capítulos e percursos editoriais.
- `content/geography/*.geojson`: geometrias com validade temporal.
- `schemas/atlas-v2.schema.json`: contrato público versionado.

SQLite não faz parte do modelo v2. Bundles de publicação serão projeções
determinísticas desses documentos.

## Checkpoint Fundação v2

```powershell
python scripts/validate_contracts.py
python scripts/migrate_sqlite.py
python scripts/validate_migration.py
python scripts/check_determinism.py
python scripts/build_bundles.py
python scripts/validate_bundles.py
python scripts/check_bundles_determinism.py
python scripts/audit_editorial_coverage.py --check
python scripts/audit_journey_coverage.py --check
python scripts/audit_story_media.py --check
```

`migrate_sqlite.py` lê o SQLite v1 somente em modo read-only e recria
`migration/` de forma determinística. A pasta contém 920 documentos de
entidade, coleções de fontes, evidências e predicates, o mapa completo de
identidades legadas, relatório de contagens e checksums SHA-256. Nenhum arquivo
em `current/atlas-web` é modificado.

`validate_migration.py` compara a projeção com as tabelas canônicas e bloqueia
perda de entidades, nomes, identificadores externos, statements, claims,
fontes, evidências, predicates, redirects ou identificadores legados.

O resultado é a migração canônica aprovada no CP20. O SQLite da v1 permanece
somente como legado rastreável e não participa do build público da v2.

## Bundles de publicação

`build_bundles.py` projeta os documentos em `bundles/`, segmentando resumos
por categoria, período e região. `manifest.json` registra caminho, contagem e
SHA-256; `journeys.json` conecta os seis percursos aprovados às entidades,
claims e fontes canônicas. O protótipo sincroniza esses arquivos no build por
meio de `npm run sync:data`.

O comando valida IDs, referências, fontes, estrutura editorial, geografia e o
round-trip JSON determinístico dos exemplos.

## Auditoria editorial transversal

`audit_editorial_coverage.py` mede todos os capítulos anuais contra entidades,
claims, fontes, mídia e geografia canônicas. O relatório determinístico em
`reports/editorial-coverage.json` separa integridade estrutural de completude
editorial e mantém os gaps como backlog explícito no CI.

`audit_journey_coverage.py` acompanha os seis percursos obrigatórios e valida
evidência, narrativa completa, mídia licenciada, geometria temporal e ativos
de apresentação. O relatório `reports/journey-coverage.json` distingue um
estado estruturalmente íntegro da conclusão editorial dos seis pacotes.

`story-media-decisions.json` registra uma decisão editorial para cada um dos
258 capítulos. `audit_story_media.py` bloqueia referências ausentes, hotlinks,
licenças não permitidas, créditos ou textos alternativos incompletos e anos sem
decisão. Uma composição `text-led` é explícita e continua contabilizada como
backlog de mídia específica, sem transformar os seis fundos temáticos em falsa
cobertura histórica individual.
