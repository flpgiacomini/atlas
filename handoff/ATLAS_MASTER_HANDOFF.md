# ATLAS — Handoff Mestre Consolidado

**Versão do handoff:** 2026-08-18  
**Objetivo:** permitir que o desenvolvimento do Atlas continue a partir de um único workspace, sem depender do histórico da conversa.

---

# 1. Resumo executivo

O Atlas evoluiu de uma ideia de “atlas genealógico global da indústria automotiva” para um sistema de conhecimento histórico com:

- modelo semântico próprio e validado;
- provenance explícita;
- tratamento de conflitos históricos;
- cronologia/validade temporal;
- veículos, empresas, marcas, pessoas, tecnologias, componentes, Motorsport, circuitos e lugares;
- banco canônico SQLite;
- pesquisa assistida por Zotero/OpenRefine/Heurist provisório;
- conteúdo representativo de 1885 ao período moderno;
- primeiro capítulo histórico completo (1885–1918);
- Content MVP global;
- protótipo funcional;
- arquitetura v1 congelada como static-first/backendless;
- scaffold Astro para o produto final;
- Pagefind previsto para busca;
- Cytoscape.js, vis-timeline e Leaflet para exploração;
- CI e fallback de deploy preparados.

A fase atual é **A9 — Atlas v1.0 / Product Complete**.

O projeto não está “no começo do desenvolvimento”. O que falta é fechar os gates operacionais e visuais da primeira versão completa.

---

# 2. Visão do produto

Definição consolidada:

> Um atlas global, histórico e explorável da indústria automobilística, centrado nos veículos e construído como uma rede de entidades, relações/fatos temporais, eventos e evidências.

A experiência desejada não é navegar por uma árvore fixa. Qualquer Entity pode servir de entrada:

```text
Vehicle
→ Organization
→ Person
→ Technology
→ another Vehicle
→ Competition
→ Entry
→ Driver
→ Circuit
→ CircuitLayout
→ Event
```

Experiências da v1:
- busca;
- Entity Page;
- relações;
- genealogia;
- timeline;
- mapa;
- grafo;
- comparação;
- evidências/fontes.

---

# 3. Princípios que orientaram o projeto

## 3.1 Não reinventar a roda
Reusar ferramentas maduras para bibliografia, reconciliação, mapa, grafo, timeline e publicação.

## 3.2 Evitar overengineering
Não construir backend, graph database, geocoder, CMS próprio ou infraestrutura persistente sem dor comprovada.

## 3.3 Veículo no centro
Empresas/pessoas/geografia explicam o veículo e sua história.

## 3.4 Complete-in-context
O Atlas não cataloga todo parafuso, trim, model year, VIN ou corrida.

## 3.5 Precisão sobre completude
Prioridade:
**PRECISÃO > UTILIDADE > VISUALIZAÇÃO > COMPLETUDE > COMPLEXIDADE**

## 3.6 Conflito histórico é dado
Duas fontes oficiais podem discordar. O sistema precisa mostrar isso, não escolher silenciosamente.

## 3.7 Views são projeções
Timeline, mapa, grafo, genealogy e compare não possuem banco paralelo.

---

# 4. Escopo congelado da v1

Tipos raiz:

- Vehicle
- VehicleInstance
- Organization
- Brand
- Person
- Technology
- Component
- Facility
- Place
- Competition
- Season
- Team
- Circuit
- CircuitLayout
- Regulation
- Event
- Entry

Níveis de Vehicle:
- family
- generation
- variant
- configuration
- standalone

Out-of-scope v1:
- modelos 3D;
- vídeo hospedado;
- telemetria/lap-by-lap;
- VIN catalogue;
- catálogo completo de trims/model years/opções;
- parts catalogue;
- engine gráfico/mapa próprio;
- mobile app nativo;
- social/community;
- auth complexa;
- graph DB obrigatório;
- ingestão indiscriminada;
- IA decidindo “verdade” automaticamente.

Referência:
`current/project-spec/ATLAS_SCOPE_FREEZE_v1.0.md`

---

# 5. Modelo canônico

## 5.1 Primitivas

```text
ENTITY
PREDICATE
STATEMENT
CLAIM
EVIDENCE
SOURCE
```

`Event` e `Entry` são Entity.

Uma relação é:

```text
Statement
subject = Entity
predicate = controlled Predicate
object_type = entity
object = Entity
```

Um fato escalar usa a mesma estrutura com:
- string;
- date;
- number;
- quantity;
- boolean.

## 5.2 Statement

Campos centrais:
- UUIDv7;
- subject;
- predicate;
- typed object;
- validity;
- qualifiers;
- confidence;
- resolution_status.

Confidence:
- high
- medium
- low
- disputed
- unknown

Resolution:
- accepted
- disputed
- unresolved
- needs_reconciliation
- rejected

## 5.3 Provenance

```text
Statement
   ↓
Claim
   ↓
Evidence
   ↓
Source
```

Claim stance:
- supports
- contradicts
- qualifies
- mentions

Support strength:
- explicit
- strong
- indirect
- weak

## 5.4 IDs

A primeira geração de pilotos usava IDs como:

```text
veh_000001
stm_000001
```

O merge mostrou colisões.

A v1 usa **UUIDv7** para:
- Entity
- Predicate
- Statement
- Source
- Claim
- Evidence

`legacy_identifier` guarda rastreabilidade dos IDs antigos.

## 5.5 Tabelas SQLite

Schema de referência possui:
- `meta`
- `entity`
- `entity_name`
- `external_identifier`
- `legacy_identifier`
- `predicate`
- `statement`
- `source`
- `claim`
- `evidence`
- `claim_evidence`
- `entity_redirect`

Views:
- `v_entity_edge`
- `v_statement_source`

Schema:
`current/canonical-model/sql/atlas_v1_schema.sql`

## 5.6 Snapshot vigente

O único banco para continuar é:

```text
current/atlas-web/data/atlas.sqlite
```

SHA-256:

```text
62392b653dec0c1ba490ebcd4fd13e7bb2cde0e5b8cdb21fafe79f01c5afa33d
```

Contagens atuais:

| Objeto | Total |
|---|---:|
| Entity | 339 |
| Statement | 446 |
| Source | 125 |
| Claim | 572 |
| Evidence | 572 |
| Predicate | 54 |
| EntityName | 14 |
| ExternalIdentifier | 2 |

Distribuição atual de Entity types:

- `brand`: 18
- `circuit`: 4
- `circuit_layout`: 6
- `competition`: 4
- `component`: 7
- `entry`: 4
- `event`: 103
- `facility`: 10
- `organization`: 30
- `person`: 35
- `place`: 4
- `team`: 3
- `technology`: 24
- `vehicle`: 82
- `vehicle_instance`: 5

---

# 6. Como o modelo foi validado

## 6.1 Porsche 917

Pressões testadas:
- family/variant;
- chassis físico;
- VehicleInstance;
- Motorsport Entry;
- drivers;
- team/entrant;
- Event;
- configuration contextual.

Conclusões:
- Entry deve ser Entity.
- Chassis 917-023 precisa ser distinguido de “Porsche 917”.
- `configured_as` é útil para um VehicleInstance representar configuração usada em determinado contexto/evento.
- O piloto revelou que `entered_by` precisa aceitar Team/Organization e que entrantes históricos podem até ser Person.
- Evidence locator inicial era genérico demais; isso virou item de qualidade.

## 6.2 Porsche 911

Pressões:
- família de longa duração;
- gerações sobrepostas;
- nomes históricos;
- predecessor/successor;
- conflito entre fontes oficiais.

Descoberta crítica:
duas páginas oficiais Porsche deram datas diferentes para a mudança 901 → 911:
- 22/10/1964;
- 22/11/1964.

O sistema preserva ambas como Statements disputados.

Conclusões:
- `successor_of` não implica fim imediato da geração anterior.
- “Generation period” não deve ser automaticamente igual a produção exata.
- não criar `VehicleLineage` até casos reais justificarem.
- aliases históricos precisam de validade/provenance.

## 6.3 Gurgel BR-800

Pressões:
- fabricante brasileiro extinto;
- component/engine;
- sucessor Supermini;
- fim corporativo ambíguo.

Descoberta:
1993 concordata, 1994 falência e 1996 fechamento/encerramento não são o mesmo fato.

Conclusão:
“fim da empresa” não pode ser um único campo.

## 6.4 Ford Model T

Pressões:
- produção em instalações diferentes;
- tecnologia de fabricação;
- mudança de fábrica;
- mass production.

Conclusão:
`produced_at` precisa de validade temporal.
Moving assembly line é Technology ligada à produção/facility.

## 6.5 Nürburgring

Pressões:
- circuito persistente;
- layouts simultâneos/históricos;
- comprimentos variáveis;
- reconstruções.

Conclusão:
Circuit e CircuitLayout são Entity types distintos.

Problema descoberto:
Nürburgring v0.1 tinha Statement IDs duplicados. Isso foi corrigido em v0.2 e ajudou a formalizar IDs globais + duplicate validation.

## 6.6 Merge dos cinco pilotos

O primeiro merge encontrou:
- IDs reutilizados em datasets;
- duplicate Statements;
- mesma Entity criada de forma independente (`Turbocharging`).

Resultado:
- namespace/migration temporária;
- depois UUIDv7;
- Entity Resolution tornou-se requisito formal.

---

# 7. Evolução quantitativa do dataset

| Marco | Entities | Statements | Sources | Claims/Evidence |
|---|---:|---:|---:|---:|
| 5-case SQLite pilot | 86 | 131 | 24 | 203 / 203 |
| A4 Diversity | 160 | 220 | 50 | 308 / 308 |
| A5 Chapter I completo | 267 | 360 | 99 | 470 / 470 |
| A7 Content MVP | 334 | 439 | 123 | 563 / 563 |
| A9 atual | **339** | **446** | **125** | **572 / 572** |

O aumento final do A9 vem da prova real:
**Volvo PV544 → Nils Bohlin → cinto de três pontos → evento de 13/08/1959**.

---

# 8. Tool Bake-Off e workspace de pesquisa

## 8.1 Problema separado em duas decisões

1. Onde pesquisar/curar confortavelmente?
2. Qual é a representação canônica/portável?

Essas respostas não precisam ser o mesmo produto.

## 8.2 Representação canônica
SQLite + CSV/JSON permanece.

## 8.3 Workspace provisório
Ordem final de teste:

1. **Heurist**
2. **Wikibase**
3. **nodegoat**
4. **Grist** fallback

### Heurist
Escolhido como primeiro hands-on por equilibrar:
- Humanidades/história;
- relações;
- temporalidade;
- mapa;
- timeline;
- network;
- filtros;
- import/export.

Risco:
Statement/Claim/Evidence pode ficar burocrático.

### Wikibase
Melhor correspondência semântica:
Item → Statement → qualifiers → references.

Risco:
administração de properties/wiki/SPARQL pode diminuir prazer de pesquisa.

### nodegoat
Ótimo semanticamente para pesquisa temporal/histórica, mas condições operacionais/hosting tornaram-no condicional.

### Grist
Fallback explícito se os outros ficarem burocráticos.

## 8.4 Ferramentas de apoio

**Zotero**
- Source library;
- web snapshots;
- bibliografia.

**OpenRefine**
- limpeza;
- deduplicação;
- reconciliation;
- Wikidata IDs;
- batch import preparation.

**Tropy**
- opcional para fotos/documentos de arquivo.

**Datasette**
- inspeção local do SQLite;
- debugging;
- JSON/SQL explorer;
- não backend do produto.

Arquivos:
`current/research-workspace/`

## 8.5 Estado real do A3

A3 foi **preparado**, mas não executado hands-on em uma conta/instância Heurist.

Isso continua sendo uma pendência real e não deve ser descrito como concluído.

---

# 9. A4 — Diversity Stress Test

Objetivo:
tentar quebrar o modelo com casos globais e estruturalmente diferentes.

Casos P0 usados:
- Benz Patent-Motorwagen;
- Toyoda Model AA;
- Hyundai Pony;
- Hongqi CA72;
- Tata Nano;
- Honda N360;
- Toyota Prius;
- Nissan LEAF;
- Audi quattro;
- ŠKODA 1000 MB;
- Holden 48-215;
- Bugatti revival chain;
- Toyota 86 / Subaru BRZ.

Âncoras pré-existentes:
- Porsche 911;
- Porsche 917;
- Gurgel BR-800;
- Ford Model T;
- Nürburgring.

Resultado:
- 13/13 PASS;
- 0 novos tipos raiz;
- 0 novos predicates;
- apenas `developed_by` expandido para aceitar Vehicle como subject.

Isso foi o gate que deu confiança para tratar Data Model v1.0 como estável.

---

# 10. A5 — Chapter I 1885–1918

Título narrativo:
**From invention to automotive industry**

Blocos construídos:

## 1885–1894
- Benz;
- Daimler;
- Peugeot;
- Panhard & Levassor;
- Benz Velo.

## 1894–1906
- Paris–Rouen;
- Vanderbilt Cup;
- Grand Prix de l'A.C.F.;
- Entry model aplicado aos primeiros eventos de Motorsport.

## 1896–1908
- Daimler commercial truck;
- Renault;
- FIAT;
- Lancia;
- Rolls-Royce;
- Oldsmobile;
- Cadillac;
- Ford.

## 1901–1913
- scale/standardization;
- Cadillac interchangeable parts;
- Model N;
- Model T;
- moving assembly line.

## 1914–1918
- Benz/DMG aeroengines;
- alteração de linhas comerciais;
- interrupções;
- Taxis de la Marne.

Resultado:
A5 foi declarado **completo para escopo v1**, não exaustivo.

Backlog permanece em:
`current/content-reference/a5/A5_POST_CHAPTER_BACKLOG.csv`

---

# 11. A6 — Functional MVP

Primeira UI executável.

Stack usada propositalmente como protótipo:

```text
SQLite
→ FastAPI read-only
→ HTML/CSS/JS
   ├ Cytoscape.js
   ├ vis-timeline
   └ Leaflet
```

Endpoints produzidos:
- `/api/stats`
- `/api/featured`
- `/api/search`
- `/api/entities/{id}`
- `/api/statements/{id}/evidence`
- `/api/graph/{id}`
- `/api/timeline`
- `/api/map`
- `/api/compare`
- `/api/path`

Funcionalidades:
- global search;
- Entity Page;
- relações;
- Evidence drawer;
- timeline;
- 2-hop graph;
- map prototype;
- compare;
- shortest-path.

Smoke test validou inclusive:
- Porsche 917;
- 911 conflict;
- evidence;
- compare;
- path Entry → Richard Attwood.

Decisão posterior:
**FastAPI não sobrevive para produção.**

Artefato:
`historical-artifacts/atlas_a6_functional_mvp_v0_1.zip`

---

# 12. A7 — Content MVP

Objetivo:
parar de parecer dataset de Porsche/Ford/pre-1918 e tornar exploração temporal/global útil.

Âncoras adicionadas:
- Citroën Traction Avant;
- Volkswagen Beetle;
- Ferrari 125 S;
- Land Rover Series I;
- Toyota Land Cruiser BJ;
- Classic Mini;
- Ford Mustang;
- Lamborghini Miura;
- Mazda Cosmo Sport;
- Volkswagen Golf I;
- Renault Espace;
- McLaren F1;
- Tesla Roadster;
- BYD F3DM;
- Toyota Mirai;
- BMW Plant Rosslyn.

Cobertura:
- Europa;
- América do Norte;
- América do Sul;
- Ásia Oriental;
- Sul da Ásia;
- Oceania;
- África industrial.

Tecnologias/contextos:
- monocoque/FWD;
- off-road;
- supercar;
- rotary;
- hatch;
- MPV;
- BEV;
- PHEV;
- fuel cell;
- global manufacturing.

Resultado:
**Content MVP PASS**.

---

# 13. A8 — Architecture Gate

Este é o principal ADR arquitetural vigente.

## Decisão

**Static-first e backendless em produção.**

Pipeline:

```text
RESEARCH
Zotero + OpenRefine + Heurist (provisional)
            ↓
CANONICAL
SQLite v1
            ↓
validation/export
            ↓
PUBLICATION
Astro static
├ Entity pages
├ graph projections
├ timeline
├ map/GeoJSON
├ compare index
└ Pagefind
            ↓
STATIC HOST
Cloudflare Pages
ou qualquer static host
```

## Decisões específicas

- Astro static;
- Pagefind;
- Cytoscape.js;
- vis-timeline;
- Leaflet;
- Datasette local;
- sem API pública;
- sem backend;
- sem Neo4j;
- Cloudflare Pages primário;
- GitHub Pages/genérico fallback.

## Scaling gates para reconsiderar backend

Somente se surgir:
- edição multiusuário no app;
- estado personalizado sincronizado;
- queries dinâmicas impossíveis de precomputar;
- build operacionalmente doloroso;
- limites reais de páginas/arquivos;
- dados mudando com frequência incompatível com rebuild.

Nenhum ocorreu ainda.

---

# 14. A9 — implementação atual

## 14.1 Fundação

Projeto atual:

```text
current/atlas-web/
```

Arquivos centrais:

### Configuração
- `package.json`
- `astro.config.mjs`
- `tsconfig.json`

### Banco/dados
- `data/atlas.sqlite`
- `data/geography.registry.json`
- `data/map-points.prototype.json`

### Build
- `scripts/export_web.py`
- `scripts/validate_dist.py`

### Layout
- `src/layouts/BaseLayout.astro`

### Components
- `CompareButton.astro`
- `Facts.astro`
- `Graph.astro`
- `Relations.astro` (primeira implementação; SemanticRelations é a direção nova)
- `SemanticRelations.astro`
- `Timeline.astro`

### Pages
- `/` → `src/pages/index.astro`
- `/e/[id]/` → `src/pages/e/[id].astro`
- `/timeline/`
- `/graph/`
- `/map/`
- `/compare/`

### Styles
- `src/styles/global.css`

### Generated publication data
- `src/data/generated/entity-pages.json`
- `src/data/generated/stats.json`
- `src/data/generated/timeline.json`
- `public/data/graph-index.json`
- `public/data/compare-index.json`
- `public/data/geography.registry.json`
- `public/data/timeline.json`

### CI
- `.github/workflows/build.yml`
- `.github/workflows/github-pages.yml`

## 14.2 `export_web.py`

Responsabilidades:
- abrir SQLite;
- parsear provenance;
- montar outgoing/incoming Statements;
- classificar relações por grupos semânticos;
- gerar grafo two-hop por Entity;
- gerar related Events;
- gerar `entity-pages.json`;
- gerar stats;
- gerar graph index;
- gerar timeline;
- gerar compare index;
- copiar geography registry.

Esse script é uma peça importante do contrato canônico → publicação.

## 14.3 Relationship UX

Agrupamentos atuais:
- genealogy;
- industry;
- people;
- technology;
- geography;
- motorsport;
- events;
- other.

Isso esconde o Predicate Registry do usuário comum sem perder semântica.

## 14.4 Evidence UX

Facts/relations mostram fonte expandível:
- title;
- publisher;
- URL;
- stance;
- support strength.

## 14.5 Compare

`CompareButton.astro` usa `localStorage`, máximo de quatro entidades.

`/compare/` usa `compare-index.json`.

Sem sessão/servidor.

## 14.6 Graph

`/graph/` usa `graph-index.json` e BFS no browser para encontrar paths de até sete saltos.

Cytoscape destaca o path.

## 14.7 Timeline

`/timeline/` possui:
- ano inicial;
- ano final;
- filtro textual.

Ainda é uma experiência simples e precisa de gate visual.

## 14.8 Geography

A9 separou:

```text
address/location truth
≠
publication geometry
```

`geography.registry.json` contém:
- address_status;
- official_address;
- address_source;
- geometry_status;
- lat/lon;
- precision;
- geometry_source;
- release_ready.

No estado atual:
- registros inicialmente preparados: 4;
- geometrias release-ready: **0**.

O map final não deve tratar pontos aproximados como canônicos.

## 14.9 Research→Publication proof

Caso novo:
- Volvo PV544;
- Nils Bohlin;
- modern three-point safety belt;
- Event em 13/08/1959.

Após adicionar ao SQLite:
- export rerodado;
- páginas: 339;
- graph edges: 332;
- timeline events: 103.

Isto prova que a publicação não está hardcoded para o conteúdo A7.

## 14.10 CI

Workflow atual executa:
1. checkout;
2. Python;
3. Node;
4. `npm install`;
5. `npm run build`;
6. `validate_dist.py`;
7. upload do `dist/`.

Após gerar lockfile real, alterar para `npm ci`.

---

# 15. O que NÃO foi efetivamente executado ainda

Importante para não criar falso senso de conclusão.

## 15.1 Astro/Pagefind build
O scaffold existe, mas `npm install` + `npm run build` não foi executado no ambiente anterior por indisponibilidade dos pacotes/rede.

## 15.2 Browser acceptance
A6 teve bloqueio de navegador local automatizado.
A9 ainda precisa de uma sessão visual real.

## 15.3 Heurist hands-on
Os imports/mappings estão prontos.
A instância e o workflow real não foram concluídos.

## 15.4 Geometrias
Endereços selecionados foram separados/registrados, mas nenhuma das quatro geometrias iniciais foi marcada release-ready.

## 15.5 Deploy real
CI/config está preparado, porém nenhuma publicação real foi registrada como gate concluído.

---

# 16. Arquivos históricos gerados

Este workspace arquiva **24 ZIPs históricos**, com aproximadamente **3.26 MiB**.

Tabela resumida:

| Artefato | Categoria | Estado | Conteúdo |
|---|---|---|---|
| `atlas_a3_research_workspace_v0_1.zip` | Research workflow | CURRENT RESEARCH REFERENCE; hands-on pending | Heurist import blueprint, Zotero structure, OpenRefine reconciliation and workflow rules. |
| `atlas_a4_seed_dataset_v0_1.zip` | A4 planning | Historical planning | 24-case diversity matrix and acceptance gates. |
| `atlas_a4_seed_validation_v0_2.zip` | A4 result | Historical milestone | 13 P0 diversity cases merged into canonical SQLite; model passed without new root types/predicates. |
| `atlas_a5_chapter1_batches_2_3_v0_2.zip` | A5 content | Historical milestone | France/Germany expansion: Renault Type A, Panhard, De Dion, Benz Velo, Mercedes 35 hp, Daimler truck. |
| `atlas_a5_chapter1_batches_4_5_v0_3.zip` | A5 content | Historical milestone | Italy/UK/USA expansion: Lancia, Silver Ghost, Oldsmobile, Cadillac, Ford Model N. |
| `atlas_a5_chapter1_complete_v0_4.zip` | A5 result | CONTENT REFERENCE | Chapter I complete for v1 scope; Motorsport origins and WWI industrial transition included. |
| `atlas_a5_chapter1_foundation_v0_1.zip` | A5 content | Historical milestone | Chapter I first historical batch (1885–1918). |
| `atlas_a6_functional_mvp_v0_1.zip` | A6 prototype | SUPERSEDED as production architecture; useful UX prototype | FastAPI + HTML/JS read-only functional exploration MVP with search, entity page, evidence, graph, timeline, map and compare. |
| `atlas_a7_content_mvp_v0_1.zip` | A7 result | CONTENT REFERENCE | Global content MVP; 334 entities and cross-era/region anchors. |
| `atlas_a8_architecture_gate_v0_1.zip` | A8 architecture | ARCHITECTURE AUTHORITY | Static-site proof and final v1 architecture decision: Astro/Pagefind/backendless. |
| `atlas_a9_foundation_v0_1.zip` | A9 implementation | SUPERSEDED by A9 v0.3 | Initial Astro scaffold and SQLite→web export pipeline. |
| `atlas_a9_product_v0_2.zip` | A9 implementation | SUPERSEDED by A9 v0.3 | Geography rules, semantic relation groups, compare UX and Volvo research→publication proof. |
| `atlas_a9_product_v0_3.zip` | A9 implementation | CURRENT CODE AUTHORITY | Latest current product code: graph path exploration, timeline filtering, CI build gate, deployment fallback. |
| `atlas_canonical_data_model_v1_0.zip` | Canonical model | SEMANTIC AUTHORITY | SQLite schema, JSON Schemas, predicate registry, UUIDv7 strategy and validator. |
| `atlas_pilot_5_cases_v0_2.zip` | Pilot consolidation | Historical reference | Bundle of five initial pilots and consolidated validation. |
| `atlas_pilot_ford_model_t_v0_1.zip` | Pilot | Historical reference | Ford Model T test: facility chronology and manufacturing technology. |
| `atlas_pilot_gurgel_br800_v0_1.zip` | Pilot | Historical reference | Gurgel BR-800 test: extinct manufacturer, successor, component and bankruptcy/closure distinction. |
| `atlas_pilot_nurburgring_v0_1.zip` | Pilot | SUPERSEDED | Initial Nürburgring circuit/layout test; contains duplicate Statement IDs later corrected. |
| `atlas_pilot_nurburgring_v0_2.zip` | Pilot | Historical reference | Corrected Nürburgring pilot with unique IDs; validates Circuit vs CircuitLayout. |
| `atlas_pilot_porsche_911_v0_1.zip` | Pilot | Historical reference | Porsche 911 lineage/generation test; overlapping generations and conflicting official rename dates. |
| `atlas_pilot_porsche_917_v0_1.zip` | Pilot | Historical reference | Porsche 917 semantic stress test: VehicleInstance, Entry, drivers/team/event, configured_as and provenance. |
| `atlas_scope_roadmap_v1_0.zip` | Scope/roadmap | REFERENCE AUTHORITY | Scope Freeze v1.0, roadmap, SQLite report and portable CSV snapshot. |
| `atlas_sqlite_bakeoff_v0_1.zip` | Data-model bakeoff | Historical reference | First merged SQLite proof and acceptance-query execution. |
| `atlas_tool_bakeoff_v0_2.zip` | Tool evaluation | REFERENCE AUTHORITY | Heurist/Wikibase/nodegoat/Grist mappings and scorecard; supporting tool shortlist. |

Para a lista literalmente completa de arquivos contidos em todos os ZIPs:
`manifests/ALL_GENERATED_FILES.csv`

Ela inclui inclusive as centenas de Entity Pages UUID geradas no POC estático A8.

---

# 17. Quais arquivos devem ser editados daqui para frente

## Produto
```text
current/atlas-web/
```

## Conteúdo
```text
current/atlas-web/data/atlas.sqlite
```

Preferencialmente alterado por processo de pesquisa/import/validação, não por edição manual casual.

## Semântica
```text
current/canonical-model/
```

Só modificar com change control.

## Pesquisa
```text
current/research-workspace/
```

## Scope
```text
current/project-spec/
```

Não reabrir sem motivo forte.

---

# 18. Estrutura deste workspace

```text
atlas_master_workspace_2026-08-18/
├ README.md
├ handoff/
│  ├ ATLAS_MASTER_HANDOFF.md
│  ├ CURRENT_STATUS.md
│  ├ DECISION_REGISTER.md
│  └ CONTINUE_FROM_HERE.md
├ current/
│  ├ atlas-web/
│  ├ canonical-model/
│  ├ project-spec/
│  ├ research-workspace/
│  ├ content-reference/
│  └ architecture-reference/
├ manifests/
│  ├ ARTIFACTS.csv
│  ├ ALL_GENERATED_FILES.csv
│  ├ CURRENT_CODE_FILES.csv
│  └ CHECKSUMS_SHA256.txt
└ historical-artifacts/
   └ todos os ZIPs anteriores
```

---

# 19. Próximo estado desejado

O próximo checkpoint ideal é:

```text
A9 v0.4
```

com:
- package-lock real;
- Astro build PASS;
- Pagefind funcionando;
- validate_dist PASS;
- primeiras geometrias release-ready;
- screenshots/validação de UI;
- Heurist hands-on concluído ou fallback decidido;
- deploy real.

Depois disso:
**A9.7 Product Complete**.

---

# 20. Definição de “acabou a v1”

A v1 não exige “todos os carros do mundo”.

A9 termina quando:
- a pesquisa entra;
- provenance permanece;
- o build é reproduzível;
- o site é navegável;
- o usuário consegue fazer sessões reais de curiosidade;
- mapa/timeline/grafo/compare são úteis;
- infraestrutura não domina o projeto.

Após isso:
- v1.x = expansão e correção de conteúdo;
- v2 = apenas se novas capacidades forem justificadas pelo uso.

---

# 21. Regra final de continuidade

**Não continuar de um ZIP antigo.**

Começar sempre por:

```text
current/atlas-web/
```

e consultar:

```text
handoff/CURRENT_STATUS.md
handoff/CONTINUE_FROM_HERE.md
handoff/DECISION_REGISTER.md
```

antes de mudar arquitetura ou modelo.

Se uma futura sessão de IA receber apenas este workspace, ela deve conseguir reconstruir o contexto técnico e prosseguir sem depender da conversa original.
