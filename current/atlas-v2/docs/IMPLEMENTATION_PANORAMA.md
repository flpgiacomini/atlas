# Panorama de implementação — Atlas v2

Atualizado em: 2026-08-21

## Estado executivo

O Atlas v2 já possui fundação canônica, migração reproduzível, bundles,
protótipo React/Astro, 258 rotas anuais, timeline global, modal e primeiras
visualizações especializadas. O acervo de publicação soma 927 entidades; o rio
de marcas possui 46 marcos documentados para 32 marcas e 17 relações temporais.

A v2 ainda não está pronta para substituir a v1. Os maiores blocos pendentes
são a escrita editorial dos 258 capítulos, a resolução dos 522 candidatos, a
cartografia histórica completa, o acervo visual por história e o acabamento das
visualizações com MapLibre e Cesium reais.

## Fase 1 — Fundação e contratos

Estado: concluída como fundação técnica; corte canônico ainda não autorizado.

Passos:

1. Manter schemas versionados para documentos, histórias e geografia.
2. Validar IDs semânticos, referências, claims, fontes e evidências.
3. Preservar mapa de identidade entre UUIDs legados e IDs v2.
4. Executar round-trip e geração determinística.

Checkpoint: todos os exemplos e documentos passam `validate_contracts.py`; a
migração é reproduzível e não apresenta perda silenciosa.

Próximo passo: ampliar os schemas quando `Season`, `Series`, `TechnologyFlow` e
novos tipos geográficos saírem do protótipo e entrarem no acervo real.

## Fase 2 — Migração e revisão canônica

Estado: migração mecânica concluída; revisão editorial em andamento.

Passos:

1. Manter as 920 entidades migradas rastreáveis ao SQLite v1.
2. Revisar cada registro, removendo descrições meramente catalográficas.
3. Resolver duplicidades, aliases, conflitos e lacunas de proveniência.
4. Promover somente registros com afirmações recuperáveis nas fontes.
5. Resolver individualmente os 522 candidatos documentados.

Checkpoint: 920/920 entidades classificadas como manter, fundir, substituir ou
retirar; 522/522 candidatos com decisão e justificativa versionada.

Próximo passo: continuar os lotes editoriais priorizando conexões necessárias
aos capítulos anuais, não a expansão indiscriminada do catálogo.

## Fase 3 — Núcleo da experiência temporal

Estado: protótipo funcional concluído; acabamento editorial pendente.

Passos:

1. Manter a timeline de 1769 a 2026 como estado global.
2. Sincronizar ano, histórico do navegador e todos os modos.
3. Suportar clique, teclado, arraste e swipe sem reprodução automática.
4. Manter modal imersivo sem criar rota pública por entidade.
5. Consolidar busca e descoberta em uma única central.

Checkpoint: 258/258 rotas funcionam sob `/atlas/`; mudança de ano atualiza
conteúdo e visualizações; navegação direta, voltar e avançar são estáveis.

Próximo passo: substituir textos provisórios das páginas anuais por capítulos
reais e testar transições longas da timeline em desktop e celular.

## Fase 4 — Visualizações especializadas

Estado: cinco projeções editoriais prototipadas; densidade e interação ainda
provisórias.

Passos:

1. Marcas: completar fundações, fusões, aquisições, renomes e encerramentos.
2. Veículos: modelar gerações, plataformas, derivações e uso em competição.
3. Competições: estruturar séries, temporadas, etapas, equipes e circuitos.
4. Eventos: construir agenda paralela de lançamentos, legislação e crises.
5. Tecnologias: registrar invenção, primeiro uso, transferência e difusão.
6. Fornecer resumo textual equivalente para cada visualização.

Checkpoint: cada modo responde ao ano global, possui estados vazio, carregando
e erro, e abre o mesmo modal editorial de entidade.

Próximo passo: expandir o rio de marcas em lotes e iniciar uma linhagem completa
de veículos, uma temporada e um fluxo tecnológico como contratos de referência.

## Fase 5 — Cartografia histórica

Estado: prova de conceito; é uma das maiores pendências do produto.

Passos:

1. Inventariar toda história com componente espacial.
2. Criar GeoJSON temporal para instalações, circuitos, cidades e corredores.
3. Registrar validade, precisão, confiança, fonte e natureza aproximada.
4. Versionar fronteiras históricas necessárias aos capítulos publicados.
5. Integrar MapLibre com fallback local simplificado.
6. Integrar Cesium de forma progressiva para o globo editorial.
7. Criar mapas estáticos narrativos para rotas e mudanças que não exigem
   interação.

Checkpoint: 100% das histórias espaciais possuem geometria validada; mapa e
globo mudam com o ano e nunca geocodificam em runtime.

Próximo passo: cartografar integralmente os seis percursos obrigatórios antes de
expandir para os demais capítulos.

## Fase 6 — Expansão editorial anual

Estado: rotas completas; 231 capítulos publicados, com cobertura contínua e
integral de 1769 a 1999.

Passos:

1. Definir tese, contexto, marcos, personagens e consequência para cada ano.
2. Diferenciar anos de grande ruptura de anos de continuidade.
3. Ligar cada bloco narrativo a claims e fontes.
4. Preservar conflitos historiográficos sem escolha silenciosa.
5. Conectar capítulos a marcas, veículos, tecnologias, competições e lugares.
6. Atualizar 2026 mensalmente, separando fatos, anúncios e planos.

Checkpoint: 258/258 anos contam uma história verificável e nenhum capítulo é
apenas rótulo, lista de fatos ou texto genérico.

para 1886–1918, com revisão de cobertura ao final de cada período.
Próximo passo: iniciar a continuidade editorial de 2000–2009 e depois avançar
para 1886–1918, com revisão de cobertura ao final de cada período.
para 1886–1918, com revisão de cobertura ao final de cada período.

## Fase 7 — Mídia e direção visual

Estado: linguagem visual prototipada; cobertura e licenciamento incompletos.

Passos:

1. Criar manifesto de mídia por história.
2. Registrar autoria, origem, licença, crédito, alt text e verificação.
3. Selecionar fotografia dominante e documentos de apoio por capítulo.
4. Gerar tamanhos responsivos e formatos eficientes.
5. Criar ilustrações originais claramente rotuladas quando necessário.
6. Validar composição editorial em desktop e versão simplificada em celular.

Checkpoint: toda história publicada possui mídia licenciada ou decisão explícita
de apresentação sem imagem; não há hotlink nem crédito ausente.

Próximo passo: fechar primeiro o pacote visual dos seis percursos obrigatórios e
usar esse padrão nos lotes anuais.

## Fase 8 — Automação e qualidade documental

Estado: validadores estruturais e determinismo ativos; verificadores editoriais
avançados ainda pendentes.

Passos:

1. Validar contratos, referências, fontes, conflitos, mídia e geografia.
2. Verificar cobertura factual e correspondência entre narrativa e fontes.
3. Detectar contradições, extrapolações e similaridade excessiva.
4. Gerar bundles segmentados e índices de busca.
5. Comparar dois builds para garantir artefatos idênticos.
6. Produzir relatório consolidado de cobertura e hashes.

Checkpoint: segunda execução sem mudança de entrada gera o mesmo manifest;
nenhuma afirmação publicada fica sem fonte recuperável.

Próximo passo: implementar os verificadores de narrativa, mídia e geografia e
incluí-los obrigatoriamente no CI.

## Fase 9 — QA, corte e lançamento

Estado: CI, build e Chrome desktop passam no protótipo; gate final não iniciado.

Passos:

1. Executar QA funcional e visual dos seis percursos obrigatórios.
2. Auditar busca, links, performance, SEO e acessibilidade de melhores esforços.
3. Validar Chrome desktop como matriz bloqueante e smoke tests móveis.
4. Publicar preview edge e candidato no GitHub Pages com o mesmo conteúdo.
5. Congelar conteúdo, registrar limitações e aprovar o corte único.
6. Substituir a v1, criar tag e release somente após todos os gates.

Checkpoint final: todos os critérios de conteúdo, geografia, mídia, build e
navegação estão verdes; a URL pública foi testada após o deploy.

Próximo passo: não iniciar o corte enquanto as fases 5, 6 e 7 permanecerem
incompletas.

## Ordem recomendada de execução

1. Continuar revisão canônica e relações de marcas em paralelo à escrita anual.
2. Fechar os seis percursos como padrão completo de conteúdo, mídia e mapa.
3. Produzir os 258 capítulos por período e resolver candidatos acionados por eles.
4. Completar visualizações especializadas com dados reais.
5. Fechar cartografia e mídia de todas as histórias.
6. Ativar validadores editoriais no CI.
7. Executar QA final, preview, corte e release.

O caminho crítico passa pelos capítulos, cartografia e mídia. A infraestrutura
já permite publicar; o trabalho restante é transformar cobertura catalográfica
em experiência histórica completa e verificável.
