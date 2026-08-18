# Retomada do hands-on Heurist A9.7

Estado em 2026-08-18: **em andamento; não aprovado**.

## Instância criada

- Heurist Huma-Num 7.2.1
- Base: `felip_atlas_a97`
- URL: <https://heurist.huma-num.fr/heurist/?db=felip_atlas_a97>
- Proprietário autenticado: Felipe Giacomini

Nenhuma senha, PIN, cookie ou token está registrado no Git.

## Estrutura confirmada

- Record type: `Atlas Entity` (`0000-112`)
- Campo textual: `Atlas UUID`
- Campo textual: `Canonical name`

## Pacote de cinco pilotos

O arquivo `current/research-workspace/a3/heurist/entities_for_heurist.csv` contém 86 entidades:

- Gurgel: 13
- Porsche 917: 28
- Nürburgring: 11
- Ford Model T: 10
- Porsche 911: 24

Os arquivos `sources_for_heurist.csv` e `statements_for_heurist.csv` completam o pacote preparado. A ordem contratada continua sendo Source → Entity → Statement.

## Próxima ação exata

Na base autenticada, abrir `Populate → Delimited text / CSV`, carregar `entities_for_heurist.csv` e mapear:

- `atlas_id` → `Atlas UUID`
- `canonical_name` → `Canonical name`

Depois criar os record types Source e Statement conforme `HEURIST_FIELD_DICTIONARY.csv`, importar os outros dois CSVs, resolver os pointers e executar a matriz 10/10 de `HEURIST_HANDS_ON_PROTOCOL.md`.

O A9.7 e a tag `v1.0.0` permanecem bloqueados até nota mínima 8/10 sem perda semântica crítica.
