# Atlas — levantamento de substância do acervo

Data: 2026-08-28
Escopo medido: `current/atlas-v2/` na v2.0.0 (commit `301aeeb`)
Base: 971 documentos canônicos, 53 bundles e o registro de 633 fontes

## Por que este documento existe

Os gates da v2 medem **cobertura**: todo ano tem capítulo, todo capítulo tem
imagem e fonte, toda entidade tem decisão de curadoria. Todas essas afirmações
são verdadeiras e estão auditadas.

Nenhum gate mede se a afirmação foi confrontada por fonte independente, se o
tipo de entidade tem evidência, ou se o que a interface exibe veio do acervo ou
de uma heurística. Este levantamento mede isso.

As contagens abaixo vieram da leitura direta dos documentos e bundles, não dos
relatórios em `reports/`. Onde divergem de um relatório, a divergência está
explicada.

## 1. A evidência é majoritariamente auto-declarada pelo fabricante

Das **868 citações** de fonte feitas por claims, classificadas pelo campo
`sourceType` declarado no registro:

| Origem | Citações | |
|---|---:|---:|
| Comunicação do próprio fabricante | 498 | 57% |
| Sem `sourceType` declarado | 129 | 14% |
| Institucional | 85 | 9% |
| Museu | 51 | 5% |
| Organização, base especializada, governo, imprensa, arquivo | 100 | 11% |

Por entidade: das **312** entidades com ao menos um claim, **176 (56%)** são
sustentadas **exclusivamente** por comunicação do próprio fabricante — newsroom,
arquivo corporativo ou publicação institucional da marca, sem nenhuma fonte
independente no conjunto.

O `EDITORIAL_ENRICHMENT_ROADMAP.md` determina confrontar fontes independentes
quando a afirmação for disputada ou promocional. O acervo, medido, não faz isso
na maioria dos casos.

Não há afirmação sem fonte: todo claim tem `sources` e `evidence`, e **zero**
referências de fonte ficam sem resolução. O problema não é ausência de
proveniência, é a independência dela.

## 2. Dois corpora sob dois padrões

| Corpus | Docs | Claims | Bloco `sources` | Contrato aplicado |
|---|---:|---:|---:|---|
| `content/entities/` | 51 | 126 | 51 | Estrito: toda entidade exige fonte; todo claim só cita fonte declarada no próprio documento |
| `migration/entities/` | 920 | 736 | 0 | Migração: IDs resolvem, sem perda, checksum determinístico |

`validate_contracts.py` aplica a regra estrita apenas a `content/entities/`. Os
920 documentos migrados são verificados por `validate_migration.py`, que garante
resolução e integridade, mas não exige fonte por documento.

A disciplina documental que define o Atlas vale hoje para **5%** dos documentos.
Os demais herdaram a garantia mais fraca da migração v1. Isso não é um defeito de
integridade; é um piso editorial diferente convivendo com o primeiro sem
distinção visível.

## 3. A evidência está concentrada em dois tipos

| Tipo | Editoriais | Com claim | Claims |
|---|---:|---:|---:|
| Event | 144 | 144 | 371 |
| Vehicle | 102 | 99 | 289 |
| Person | 50 | 26 | 56 |
| Technology | 38 | 4 | 11 |
| Organization | 37 | 4 | 8 |
| Brand | 24 | 2 | 2 |
| Facility | 10 | 2 | 5 |
| Component | 9 | 4 | 5 |
| CircuitLayout | 6 | 6 | 15 |
| VehicleInstance | 5 | 5 | 11 |
| Entry | 4 | 4 | 56 |
| Circuit | 4 | 0 | 0 |
| Series | 4 | 0 | 0 |
| Place | 4 | 1 | 1 |
| Team | 3 | 0 | 0 |

Event e Vehicle concentram **660 dos 862 claims**. Marcas, tecnologias,
organizações e competições existem quase exclusivamente como nomes.

Das 506 marcas do índice, **482 são catalográficas**, 61 têm marco temporal,
17 têm relação corporativa datada e **2** têm `yearStart`.

## 4. Três modos da interface inferem fatos em runtime

Consequência direta do item 3. `src/ui/SpecializedView.jsx` define:

    const COMPETITION_PATTERN = /prix|rally|rali|race|racing|le mans|zeltweg|.../i;
    const TECHNOLOGY_PATTERN  = /turbo|hybrid|electric|motor|radar|safety|aero|.../i;

Os modos **Competições** e **Tecnologias** são populados casando essas expressões
contra o *nome* das entidades. Não há dado estruturado por trás: a view deduz o
fato a partir de substring.

`CONTINUE_FROM_HERE.md` lista entre as regras preservadas "não inferir geografia
ou fatos em runtime". A aplicação contraria essa regra exatamente onde o acervo
está vazio.

## 5. O campo `region` é rótulo de lote de curadoria, não geografia

**401 das 444** entidades editoriais têm `region = "Global / não classificado"`.
As catalográficas carregam rótulos como "Coreia China Taiwan",
"Europa 1919-1945", "Itália esportiva e artesanal" e "Pioneiras globais", que são
ondas de trabalho da curadoria e não procedência.

A interface exibe esse campo como se fosse lugar: em cada linha da busca, no
cabeçalho do modal de entidade e como as raias do rio genealógico no modo Marcas.
A leitura geográfica oferecida pelo produto é, na prática, um mapa do processo de
curadoria.

## 6. Os 258 capítulos anuais se apoiam em 88 entidades

Cada capítulo referencia uma entidade; há **88 distintas** para 258 capítulos.
As mais reaproveitadas:

| Entidade | Anos sustentados |
|---|---:|
| `atlas:event:fardier-preservation-1771-1800` | 30 |
| `atlas:event:road-mobility-transition-1841-1859` | 19 |
| `atlas:vehicle:veiculo-experimental-de-rivaz` | 18 |
| `atlas:event:hancock-steam-services-1829-1836` | 8 |
| `atlas:event:locomotive-act-1865-regime` | 8 |

Apenas **81 capítulos** têm um claim cuja validade **começa** no próprio ano.
`audit_editorial_coverage.py` reporta 134 por um critério mais amplo — qualquer
ponto de validade coincidindo com o ano, inclusive o de término — e outros 80 se
sustentam só por continuidade entre marcos (`chapterKind = "continuity"`).

Densidade por década, pelo critério estrito de claim que começa no ano:

| Décadas | Capítulos sustentados |
|---|---|
| 1780s, 1800s, 1810s, 1890s, 1900s | 0 de 10 |
| 1770s, 1830s, 1870s, 1880s | 2 de 10 |
| 1820s, 1920s | 3 de 10 |
| 1860s, 1940s, 1960s | 4 de 10 |
| 1950s, 1980s | 5 de 10 |
| 1970s | 6 de 10 |
| 1990s | 7 de 10 |
| 2000s, 2010s, 2020s | todos |

O acervo é denso no período documentável por comunicação corporativa recente e
vazio onde a história do automóvel começa.

## 7. A auditoria de mídia mede a camada que o build descarta

`reports/editorial-coverage.json` registra `uniquePresentationAssets: 6` e
atribui `people-industry.webp` a 94 anos e `technology.webp` a 91. Esse é o campo
`asset` de `content/annual-chapters.json`, um placeholder.

`scripts/build_bundles.py:151` substitui o hero pela primeira mídia resolvida do
capítulo, e o bundle publicado usa **37 imagens distintas**.

O gate está verde medindo um valor que nunca chega ao ar, e nenhum gate mede o
que chega.

## 8. Três quartos do registro de fontes não sustenta claim

Das **633** fontes do registro canônico, **472 nunca são citadas por um claim**.
São as referências individuais das 522 marcas catalográficas.

**415 (65%)** do registro é Wikipedia ou Wikidata, classificado como
`trust: institutional`.

## Leitura geral

O Atlas realiza sua tese num núcleo de cerca de 300 entidades, majoritariamente
eventos e veículos, com peso forte em Porsche e Le Mans, apoiado sobretudo na
comunicação dos fabricantes. Em volta desse núcleo há uma casca catalográfica de
522 registros e uma interface que preenche os vazios com heurística de regex e
com rótulos de lote exibidos como geografia.

Nada disso invalida os checkpoints CP19 a CP21: eles mediram o que se propuseram
a medir. O que este documento registra é que cobertura auditada e substância
histórica são grandezas diferentes, e que a v2 fechou a primeira.

## Caminhos possíveis

Independentes entre si; a ordem abaixo é uma recomendação, não uma decisão.

### A · Parar de inferir

Remover as heurísticas de `COMPETITION_PATTERN` e `TECHNOLOGY_PATTERN` e exibir
Competições e Tecnologias pelo que o acervo sustenta, ou não exibir. Separar
procedência real de lote de curadoria no campo `region`, ou parar de apresentá-lo
como lugar.

É trabalho de código, cabe em uma sessão, e faz a aplicação parar de afirmar mais
do que o acervo sustenta. Também elimina a contradição com a regra de não inferir
fatos em runtime.

### B · Decidir a superfície do produto

As 522 entidades catalográficas pertencem ao artefato público ou a um registry
separado? Os 177 capítulos sem claim próprio são capítulos ou contexto?

É decisão de escopo, não tarefa técnica. A distinção editorial/catálogo passou a
ser visível na interface em 2026-08-28, o que dá instrumentação para decidir com
o acervo à vista.

### C · Sanear a fonte

Diversificar as 176 entidades sustentadas apenas por comunicação do fabricante e
reclassificar o `trust` das 415 fontes Wikipedia/Wikidata.

É o de maior valor histórico e o mais lento: trabalho editorial contínuo, não uma
tarefa com fim.

## Reprodução das contagens

As medições foram feitas por leitura direta dos documentos, com estas definições:

- **Citação de fonte**: cada ocorrência em `claim.sources`, contada com repetição.
- **Fabricante**: `sourceType` em `manufacturer`, `manufacturer_archive`,
  `manufacturer_regional`, `manufacturer_publication` ou `corporate_archive`.
- **Sustentada só pelo fabricante**: o conjunto dos `sourceType` de todos os
  claims da entidade está contido no conjunto acima.
- **Claim no ano exato**: `claim.validity.from` começa com o ano do capítulo.
  Critério mais estrito que o de `audit_editorial_coverage.py`.
- **Nível editorial**: `metadata.editorial_level` do documento, projetado como
  `editorialLevel` nos bundles.

Nenhum desses cálculos está versionado como script. Se algum deles deve virar
gate, precisa primeiro virar script determinístico em
`current/atlas-v2/scripts/`.
