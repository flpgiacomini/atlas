# Panorama de implementação — Atlas v2

Atualizado em: 2026-08-25

## Estado executivo

O Atlas v2 possui uma cadeia reproduzível de documentos canônicos para bundles
e aplicação Astro/React. São **966 entidades publicáveis**, **52 bundles**,
**258 capítulos anuais** cobrindo 1769–2026, seis percursos editoriais, timeline
global, modal, busca e cinco visualizações especializadas. A migração preserva
os 920 registros da v1; 47 entidades editoriais adicionais foram incorporadas,
com uma sobreposição de identidade resolvida no índice final.

A cobertura anual ainda não equivale à completude histórica. A auditoria atual
confirma 258 capítulos com suporte temporal canônico e nenhum gap de alinhamento
de claims. Os capítulos usam seis ativos visuais de apresentação, somente uma
geometria temporal está publicada e não há manifesto licenciado de mídia por
história. A v2 permanece paralela à v1 e não está autorizada para o corte.

## Indicadores verificáveis

- Anos com capítulo: 258/258.
- Entidades no índice: 966 (444 editoriais e 522 catalográficas).
- Entidades referenciadas pelos capítulos: 88.
- Capítulos com claim no ano exato: 133/258.
- Capítulos com continuidade entre marcos documentados: 81/258.
- Capítulos com suporte temporal total: 258/258.
- Capítulos a alinhar temporalmente: 0/258.
- Capítulos com arquivo visual existente: 258/258; ativos únicos: 6.
- Capítulos ligados à geometria publicada: 1/258; inventário espacial pendente: 257.
- Marcos de marcas: 46; relações corporativas temporais: 17.
- Percursos editoriais obrigatórios: 6/6 estruturados.
- Migração legada: 920/920 documentos rastreáveis.

O relatório reproduzível está em `reports/editorial-coverage.json` e é validado
no CI por `scripts/audit_editorial_coverage.py --check`.

## Fase 1 — Fundação e contratos

Estado: **concluída** como fundação técnica; corte ainda não autorizado.

Entregue: schemas versionados, IDs semânticos, mapa de identidade do legado,
validação de referências, round-trip e geração determinística.

Checkpoint de saída: todos os documentos passam `validate_contracts.py`,
`validate_migration.py` e os testes de determinismo.

Restante: especializar contratos de temporadas, séries, fluxo tecnológico e
novas geometrias conforme os acervos deixarem o protótipo.

## Fase 2 — Migração e revisão canônica

Estado: **migração concluída; curadoria parcial**.

Entregue: 920 documentos migrados sem perda silenciosa e índice final com 966
entidades. O catálogo contém 522 registros no nível `catalog`; os candidatos da
v1 possuem decisões operacionais, mas sua promoção a conteúdo editorial é fila
de aprofundamento, não um gate satisfeito.

Checkpoint de saída: cada entidade catalográfica com decisão versionada —
aprofundar, manter como contexto, fundir ou retirar — e justificativa/fonte ao
ser promovida.

Próximo lote: entidades necessárias aos seis percursos completos.

## Fase 3 — Núcleo da experiência temporal

Estado: **protótipo funcional concluído; QA profundo pendente**.

Entregue: 258 rotas, ano global, histórico do navegador, timeline por
clique/teclado/arraste, modal sem rota própria e central de descoberta.

Checkpoint de saída: navegação direta, voltar/avançar, transições longas,
teclado e viewport móvel aprovados nos seis percursos e anos-limite.

Restante: testes sistemáticos de interação e acabamento responsivo.

## Fase 4 — Visualizações especializadas

Estado: **cinco modos prototipados; densidade documental incompleta**.

Entregue: projeções de marcas, veículos, competições, eventos e tecnologias,
conectadas ao ano global e ao modal. O rio de marcas possui 46 marcos e 17
relações temporais.

Checkpoint de saída: cada modo com dados reais suficientes, estados
vazio/carregando/erro e alternativa textual equivalente.

Restante: completar linhagens, temporadas, agentes e fluxos; validar transições.

## Fase 5 — Cartografia histórica

Estado: **prova de conceito; gate crítico aberto**.

Entregue: contrato GeoJSON temporal, uma rota narrativa da Porsche 917 e
componente de mapa/globo com carregamento progressivo.

Checkpoint de saída: inventário explícito de histórias espaciais e 100% desse
subconjunto com geometria, validade, precisão, confiança e fonte; MapLibre,
Cesium e fallback estático verificados sem geocoding em runtime.

Restante: classificar os 258 capítulos e cartografar os seis percursos primeiro.

## Fase 6 — Expansão editorial anual

Estado: **cobertura e gate temporal concluídos; revisão semântica em andamento**.

Entregue: 258/258 capítulos com título, narrativa, fontes, entidades e navegação
contínua. O capítulo de 2026 distingue fatos confirmados de projeções.

Checkpoint de saída: 258/258 capítulos com afirmação recuperável no ano ou
intervalo correspondente, conflitos preservados e sem extrapolação não marcada.

Restante: aprofundar anos de baixa densidade e revisar a correspondência
narrativa–evidência bloco a bloco.

## Fase 7 — Mídia e direção visual

Estado: **concluída — cobertura editorial contínua de 1769 a 2026**.

Entregue: linguagem de revista automotiva e cobertura técnica de imagem para
todos os capítulos por seis ativos temáticos.

Checkpoint de saída: cada história com mídia licenciada ou decisão explícita de
apresentação sem imagem; autoria, origem, licença, crédito, alt e verificação;
nenhum hotlink.

Entregue adicionalmente no CP16: manifesto versionado e primeiro pacote
completo, **Porsche 917 / 1969**, com arquivo local, licença, crédito, alt e
distinção explícita entre ilustração editorial e documento histórico.

Entregue no início do CP18: decisões versionadas para **258/258** histórias,
auditoria de direitos e arquivos integrada ao CI e mídia conectada aos bundles
anuais. A linha de base honesta é **6/258** capítulos com mídia específica e
**252/258** composições textuais temporárias; nenhuma reutilização temática é
contada como cobertura individual.

Lote V01 concluído: **117/117** capítulos de 1769–1885 receberam cinco quadros
editoriais originais de período. A cobertura total avançou para **123/258** e o
backlog caiu para **135** capítulos. Os ativos específicos passam a controlar o
hero anual; sobreposições cartográficas só aparecem quando classificadas como
mapa no manifesto.

Lote V02 concluído: **33/33** capítulos de 1886–1918 receberam cinco novos
quadros editoriais, preservando as mídias específicas de 1886 e 1908. A
cobertura total avançou para **154/258** e o backlog caiu para **104**.

Lote V03 concluído: **27/27** capítulos de 1919–1945 receberam cinco quadros
editoriais sobre reconstrução, design, crise, mobilidade popular e interrupção
da produção civil. A cobertura total avançou para **181/258** e o backlog caiu
para **77**.

Lote V04 concluído: **28/28** capítulos de 1946–1973 receberam cinco quadros
editoriais, complementando os percursos específicos já existentes. A cobertura
é agora contínua de 1769 a 1973, totaliza **205/258** e deixa **53** capítulos
no backlog.

Lote V05 concluído: **26/26** capítulos de 1974–1999 receberam cinco quadros
editoriais sobre eficiência, eletrônica, segurança, globalização e hibridização.
A cobertura é contínua de 1769 a 1999, totaliza **231/258** e deixa **27**
capítulos no backlog.

Lote V06 concluído: **27/27** capítulos de 2000–2026 receberam seis quadros
editoriais sobre hibridização, crise, eletrificação, software, pandemia,
política industrial e o cenário contemporâneo. A cobertura agora é contínua
de 1769 a 2026, totaliza **258/258**, com **38** itens licenciados no manifesto,
zero hotlinks e **nenhum capítulo no backlog**. Ver
[`MEDIA_CHECKPOINT_18_V06_COMPLETE.md`](MEDIA_CHECKPOINT_18_V06_COMPLETE.md).

Restante nesta fase: **nenhum gate de cobertura**. O refinamento visual futuro
é incremental e não reabre o CP18.

## Fase 8 — Automação e qualidade documental

Estado: **validação estrutural forte; validação semântica parcial**.

Entregue: validações de contratos, migração, capítulos, marcas, bundles,
referências, arquivos, determinismo e auditoria transversal no CI.

Checkpoint de saída: narrativa recuperável nas fontes, conflitos detectados,
mídia/geografia validadas e segunda geração byte a byte idêntica.

Restante: verificadores texto–fonte, extrapolação, similaridade, mídia e
inventário geográfico.

## Fase 9 — QA, corte e lançamento

Estado: **CI e Pages verdes no checkpoint anterior; gate final não autorizado**.

Entregue: build em `/atlas/`, deploy automatizado e validação Chrome desktop do
protótipo. A v1 continua preservada.

Checkpoint final: seis percursos aprovados, busca, links, performance, SEO,
Chrome e smoke mobile verdes; mídia, cartografia e evidência sem bloqueios; URL
pública verificada após deploy.

Restante: repetir QA após conteúdo, publicar candidato, cortar e criar release.

## Caminho crítico e checkpoints seguintes

1. **CP15 — Evidência temporal: concluído**, com 258/258 e zero gaps.
2. **CP16 — Seis percursos completos: concluído (6/6).** Benz / 1886,
   Model T / 1908, Origens do Motorsport / 1955, Volvo PV544 / 1958,
   Porsche 911 / 1963 e Porsche 917 / 1969 estão completos. Ver
   [`JOURNEYS_CHECKPOINT_16_COMPLETE.md`](JOURNEYS_CHECKPOINT_16_COMPLETE.md).
3. **CP17 — Inventário cartográfico: concluído.** Os 258 capítulos estão
   classificados: 95 exigem interação e 163 aceitam representação estática;
   95/95 interativos têm geometria temporal válida e não há pendências. O inventário
   está em [`CARTOGRAPHY_CHECKPOINT_17_INVENTORY.md`](CARTOGRAPHY_CHECKPOINT_17_INVENTORY.md)
   e o primeiro lote em
   [`CARTOGRAPHY_CHECKPOINT_17_PROGRESS_01.md`](CARTOGRAPHY_CHECKPOINT_17_PROGRESS_01.md)
   e o segundo em
   [`CARTOGRAPHY_CHECKPOINT_17_PROGRESS_02.md`](CARTOGRAPHY_CHECKPOINT_17_PROGRESS_02.md).
   O terceiro lote está em
   [`CARTOGRAPHY_CHECKPOINT_17_PROGRESS_03.md`](CARTOGRAPHY_CHECKPOINT_17_PROGRESS_03.md).
   O quarto lote está em
   [`CARTOGRAPHY_CHECKPOINT_17_PROGRESS_04.md`](CARTOGRAPHY_CHECKPOINT_17_PROGRESS_04.md).
   O encerramento está em
   [`CARTOGRAPHY_CHECKPOINT_17_COMPLETE.md`](CARTOGRAPHY_CHECKPOINT_17_COMPLETE.md).
4. **CP18 — Mídia editorial: concluído.** As 258 histórias têm decisão e mídia
   local licenciada, com cobertura contínua de 1769 a 2026 e backlog zero. Ver
   [`MEDIA_CHECKPOINT_18_V06_COMPLETE.md`](MEDIA_CHECKPOINT_18_V06_COMPLETE.md).
5. **CP19 — Curadoria canônica: concluído.** A fila foi reconciliada como 482
   marcas e 40 candidatos históricos. C01–C03 resolveram os primeiros 16 itens;
   C04 e C05 encerraram os 24 restantes. Os **40/40 candidatos históricos**
   estão resolvidos: 33 promovidos e sete preservados no catálogo. O C06
   encerrou integralmente a onda M01: **29/29** candidatos receberam
   decisão e **41/41** marcas do universo pioneiro estão cobertas na genealogia
   temporal, com **27 promoções** e **2 retenções**.
   C07–C17 resolveram as 453 marcas restantes. O resultado final é **522/522**:
   **471 promoções**, **51 retenções** e fila restante zero. Não há IDs
   duplicados nem entidades migradas ausentes. Ver
   [`CURATION_CHECKPOINT_19_INVENTORY.md`](CURATION_CHECKPOINT_19_INVENTORY.md),
   [`CURATION_CHECKPOINT_19_C01.md`](CURATION_CHECKPOINT_19_C01.md),
   [`CURATION_CHECKPOINT_19_C02.md`](CURATION_CHECKPOINT_19_C02.md),
   [`CURATION_CHECKPOINT_19_C03.md`](CURATION_CHECKPOINT_19_C03.md),
   [`CURATION_CHECKPOINT_19_C04.md`](CURATION_CHECKPOINT_19_C04.md) e
   [`CURATION_CHECKPOINT_19_C05.md`](CURATION_CHECKPOINT_19_C05.md) e
   [`CURATION_CHECKPOINT_19_C06_COMPLETE.md`](CURATION_CHECKPOINT_19_C06_COMPLETE.md) e
   [`CURATION_CHECKPOINT_19_C07_C17_COMPLETE.md`](CURATION_CHECKPOINT_19_C07_C17_COMPLETE.md).
6. **CP20 — QA candidato:** semântica, visualizações, Chrome, mobile e performance.
7. **CP21 — Corte v2:** Pages, smoke público, relatório, tag e release.

O caminho crítico agora é **C18 → QA → corte v2**. Infraestrutura,
seis percursos, cartografia e cobertura de mídia estão fechados; falta resolver
os candidatos catalográficos e elevar a verificação semântica antes do candidato.
