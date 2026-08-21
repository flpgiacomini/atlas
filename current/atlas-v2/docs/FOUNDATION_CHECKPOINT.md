# Checkpoint — Fundação canônica v2

Data: 2026-08-21  
Estado: aprovado como candidato de migração  
SQLite v1: preservado e lido somente em modo read-only

## Contratos congelados

O schema `atlas-v2.schema.json`, versão 2.0.0, registra os contratos de Entity,
Claim, Source, Evidence, Story, Chapter, StoryBeat, Season, Series,
TechnologyFlow e TemporalGeometry. IDs públicos seguem
`atlas:<tipo>:<slug-estavel>`.

## Resultado da projeção integral

| Objeto legado | Migrado |
|---|---:|
| Entities | 920 |
| Entity names | 14 |
| External identifiers | 525 |
| Statements | 610 |
| Claims | 736 |
| Sources | 165 |
| Evidence | 737 |
| Predicates | 56 |
| Legacy identifiers | 648 |
| Redirects | 0 |

Hash SHA-256 do SQLite:
`0034e7a0368a61a7eab7de55ddb37a5854236894eb52c36c8a318b7b1b3d053f`.

## Garantias verificadas

- IDs semânticos únicos e estáveis, incluindo tratamento determinístico de
  colisões de slugs.
- Relações entre subjects e objects resolvidas.
- Claims conectadas às fontes e evidências correspondentes.
- Stance, support strength, confidence, resolution status, validade,
  qualifiers e locators preservados.
- Nomes, aliases, identificadores externos e registry de predicates
  preservados.
- Mapa completo entre IDs legados e IDs v2 versionado.
- 925 arquivos cobertos por checksums SHA-256.
- Segunda geração sem alteração de entrada produziu o mesmo manifesto de
  checksums.

## Comandos de reprodução

```powershell
cd current/atlas-v2
python scripts/validate_contracts.py
python scripts/migrate_sqlite.py
python scripts/validate_migration.py
python scripts/check_determinism.py
```

## Próximo gate

O próximo checkpoint é transformar a projeção em bundles segmentados por
período, categoria e região, acrescentar testes automatizados no CI e conectar
os seis percursos do protótipo aos documentos migrados. O SQLite permanece
autoridade da v1 até a equivalência editorial e funcional da v2 ser aprovada.
