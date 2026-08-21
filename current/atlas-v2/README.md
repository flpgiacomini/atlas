# Atlas v2 — workspace paralelo

Este diretório contém a nova autoridade documental do Atlas. O site público em
`current/atlas-web` permanece intocado até o corte formal da v2.

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
```

`migrate_sqlite.py` lê o SQLite v1 somente em modo read-only e recria
`migration/` de forma determinística. A pasta contém 920 documentos de
entidade, coleções de fontes, evidências e predicates, o mapa completo de
identidades legadas, relatório de contagens e checksums SHA-256. Nenhum arquivo
em `current/atlas-web` é modificado.

`validate_migration.py` compara a projeção com as tabelas canônicas e bloqueia
perda de entidades, nomes, identificadores externos, statements, claims,
fontes, evidências, predicates, redirects ou identificadores legados.

O resultado atual é um **candidato de migração**. A v1 continua pública e o
SQLite só poderá ser retirado depois da revisão editorial e do gate formal de
corte da v2.

## Bundles de publicação

`build_bundles.py` projeta os documentos em `bundles/`, segmentando resumos
por categoria, período e região. `manifest.json` registra caminho, contagem e
SHA-256; `journeys.json` conecta os seis percursos aprovados às entidades,
claims e fontes canônicas. O protótipo sincroniza esses arquivos no build por
meio de `npm run sync:data`.

O comando valida IDs, referências, fontes, estrutura editorial, geografia e o
round-trip JSON determinístico dos exemplos.
