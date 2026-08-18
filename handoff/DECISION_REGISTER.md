# ATLAS — Registro de Decisões Consolidado

Este arquivo resume as decisões que devem ser tratadas como vigentes ao retomar o projeto.

## D-001 · Natureza do produto
O Atlas é um projeto pessoal de pesquisa, curiosidade e exploração da história da indústria automotiva mundial. Não é uma enciclopédia tradicional, TCC, produto SaaS ou sistema corporativo.

## D-002 · Objeto central
O veículo continua sendo o principal objeto de exploração. Empresas, marcas, pessoas, tecnologias, competições, circuitos, lugares e fontes existem para explicar e conectar veículos — sem deslocar o centro do produto.

## D-003 · Princípio de escopo
“Completo no contexto, não completo em cada detalhe existente.” Só entra granularidade que aumente compreensão histórica, técnica, comercial, cultural, esportiva, geográfica ou genealógica.

## D-004 · Primitivas semânticas
As primitivas canônicas são:
- Entity
- Predicate
- Statement
- Claim
- Evidence
- Source

Event e Entry são tipos de Entity. Uma relação é um Statement cujo objeto é outra Entity.

## D-005 · Tipos raiz congelados para v1
vehicle, vehicle_instance, organization, brand, person, technology, component, facility, place, competition, season, team, circuit, circuit_layout, regulation, event, entry.

Novos tipos raiz só entram se ao menos dois casos reais não puderem ser representados com as primitivas existentes e houver benefício material de pesquisa/navegação.

## D-006 · Hierarquia de veículos
Os níveis family, generation, variant, configuration e standalone são representados por `Vehicle` + `vehicle_level`; não existem tabelas raiz separadas para cada nível.

## D-007 · Organization ≠ Brand
Marca e organização jurídica/corporativa são conceitos diferentes. Mudanças de proprietário, renascimentos e descontinuidades corporativas não devem apagar a continuidade histórica de uma Brand.

## D-008 · Circuit ≠ CircuitLayout
A identidade do circuito persiste enquanto layouts mudam no tempo. Comprimento/configuração pertencem ao layout, não necessariamente ao Circuit.

## D-009 · Provenance
Fato histórico importante deve poder seguir:
Statement → Claim → Evidence → Source.
Conflitos não são sobrescritos; podem coexistir Statements concorrentes com `resolution_status`.

## D-010 · Datas e validade
Nunca inventar precisão. `occurred_on`/Event representa ocorrência; `valid_from`/`valid_until` representam validade temporal de relações/estados.

## D-011 · Identidade
IDs canônicos são UUIDv7. Slug e nome são mutáveis e nunca são foreign keys. IDs externos (Wikidata, OSM, FIA, RSC etc.) ficam em `external_identifier`.

## D-012 · Predicate Registry
Predicates são controlados. Qualifier deve ser preferido a um novo Predicate quando o conceito não traz ganho recorrente de consulta/navegação.

## D-013 · Modelo físico canônico
SQLite é a implementação física canônica de referência para v1. CSV/JSONL são formatos de intercâmbio. Não há graph database obrigatório.

## D-014 · Entity Resolution
Reconciliação é obrigatória. O merge dos pilotos já detectou identidade duplicada (por exemplo Turbocharging), portanto rótulo igual ou score externo nunca decide merge automaticamente.

## D-015 · Workspace de pesquisa
Stack provisória:
Zotero → OpenRefine → Heurist → SQLite canônico.
Heurist é o candidato operacional, não a autoridade canônica. O hands-on do workspace ainda precisa ser validado.

## D-016 · Ferramentas alternativas
Wikibase é o benchmark semântico; nodegoat é benchmark histórico/temporal condicionado a elegibilidade/self-hosting; Grist é a saída simples se os demais forem burocráticos.

## D-017 · Timeline, mapa, grafo, genealogia e compare
São projeções derivadas do modelo canônico. Não criar bases paralelas de timeline, mapa ou grafo.

## D-018 · A5
O período 1885–1918 foi declarado completo para o escopo v1 quando se tornou historicamente explorável; catálogo exaustivo não é gate.

## D-019 · A7
O Content MVP privilegia diversidade histórica e geográfica, não quantidade bruta de veículos.

## D-020 · Arquitetura web v1
Atlas v1 é static-first e backendless em produção:
SQLite → validação/export → Astro → Pagefind → HTML/CSS/JS/JSON/GeoJSON → hospedagem estática.

## D-021 · Backend
FastAPI do A6 foi um adaptador descartável. Não é arquitetura final. Datasette é opcional/local para inspeção e debugging.

## D-022 · Frontend
Astro static + TypeScript/JavaScript. Não adotar React/Vue/Svelte para o app inteiro sem necessidade concreta; componentes interativos continuam leves.

## D-023 · Busca
Pagefind é a busca v1, gerada depois do build estático. Não usar serviço externo de busca enquanto isso for suficiente.

## D-024 · Grafo
Cytoscape.js permanece. O modelo canônico continua relacional/Statement-based em SQLite. Neo4j só volta à discussão se uma limitação medida aparecer.

## D-025 · Timeline
vis-timeline permanece como componente de visualização derivada.

## D-026 · Mapa
Leaflet permanece em v1. MapLibre + PMTiles só entram se vetores, geometrias históricas complexas ou escala justificarem.

## D-027 · Geografia
Endereço/localização institucional e geometria de mapa são camadas distintas. Coordenada aproximada não vira canônica por conveniência. Runtime geocoding é proibido no v1.

## D-028 · Hosting
Cloudflare Pages é a opção primária; GitHub Pages/qualquer static host é fallback. Nenhuma função Cloudflare específica é requisito da v1.

## D-029 · API pública
Não existe necessidade de API pública em v1. Artefatos estáticos são a interface. API só entra por necessidade futura comprovada.

## D-030 · A9
A9 significa Atlas v1.0 / Product Complete, não apenas MVP. Depois de A9, o trabalho vira v1.x de conteúdo/qualidade e um eventual v2 opcional.

## D-031 · Regra de retomada
O código atual deve partir de `current/atlas-web/` deste workspace. Bancos dos pilotos/A4/A5/A6/A7 são snapshots históricos e não devem receber novas alterações.
