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
```

O comando valida IDs, referências, fontes, estrutura editorial, geografia e o
round-trip JSON determinístico dos exemplos.
