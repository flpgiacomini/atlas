# Atlas — Plano Mestre de Conclusão Integral

**Versão:** 1.0

**Baseline:** 20 de agosto de 2026

**Banco canônico:** `current/atlas-web/data/atlas.sqlite`

**Produto publicado:** <https://flpgiacomini.github.io/atlas/>

**Objetivo:** conduzir o Atlas do estado atual até a conclusão editorial, funcional, visual e operacional dentro do escopo aprovado.

---

## 1. Definição de “100% concluído”

“100% concluído” significa que **todo elemento aprovado para o escopo público do Atlas** foi pesquisado, reconciliado, modelado, evidenciado, conectado, ilustrado, revisado e publicado, e que todas as experiências do produto passaram pelos gates finais.

Não significa catalogar todos os trims, anos-modelo, VINs, peças, voltas, resultados esportivos ou aproximadamente 15 mil nomes comerciais encontrados em diretórios externos. O universo de conclusão é o conjunto que passar pelo gate de relevância histórica do Atlas.

O produto final exige simultaneamente:

1. nenhuma Entity pública apenas catalográfica ou sem decisão editorial;
2. 100% das Entities públicas classificadas como `complete` pela auditoria vigente;
3. 100% dos statements históricos importantes com claim e evidence;
4. 100% das mídias locais, atribuídas, licenciadas e acessíveis;
5. cobertura narrativa de 1769–1885 e de cada ano entre 1886 e 2026;
6. todas as marcas aprovadas com história, genealogia e modelos relevantes conectados;
7. automóveis de passageiros como eixo principal, com competição e tecnologia integradas;
8. caminhões, ônibus, motocicletas, fornecedores e legislação apenas quando explicarem diretamente a história principal;
9. busca, páginas, marcas, anos, grafo, timeline, mapa, comparação e fontes funcionando como projeções do SQLite;
10. CI, acessibilidade, navegadores, performance, links, deploy, documentação e release aprovados.

Qualquer item que não atingir esse piso deve ser excluído do artefato público, mantido como candidato privado/registry ou acompanhado por decisão formal de `context_only`, `hold` ou `exclude`.

---

## 2. Estado atual verificável

### 2.1 Inventário canônico

| Métrica | Atual |
|---|---:|
| Entities | 920 |
| Statements | 610 |
| Sources | 165 |
| Claims | 736 |
| Evidence | 737 |
| Predicates controlados | 56 |
| Entities editoriais | 398 |
| Entities catalográficas | 522 |
| Catálogo com fonte individual R01 | 6 |
| Editorialmente completas | 146 |
| Editorialmente substanciais | 252 |
| Marcas | 504 |
| Marcas catalográficas | 482 |
| Veículos | 142 |
| Veículos catalográficos | 40 |
| Eventos | 105 |
| Anos representados entre 1886 e 2026 | 60/141 |
| Geometrias release-ready | 4/4 |
| Mídia obrigatória atual | 398/398 |
| Testes automatizados | 12/12 |
| Entity Pages | 920 |
| Páginas pesquisáveis | 921 |

### 2.2 Situação do produto

| Área | Estado | Leitura correta |
|---|---|---|
| Arquitetura static-first | concluída | não reabrir sem change control |
| SQLite e modelo semântico | concluídos | autoridade canônica preservada |
| CI e GitHub Pages | concluídos | pipelines verdes no `main` |
| Busca e visualizações | funcionais | precisam de QA e UX sobre o acervo expandido |
| A9.7 original | aprovado | aprovação referente ao baseline anterior à expansão |
| Catálogo MASS01 | concluído | cobertura não equivale a profundidade editorial |
| Verificação R01 | concluída | 6 veículos têm primeira fonte individual |
| Marcas | cobertas nominalmente | maioria ainda sem história completa |
| Cronologia | parcial | 81 anos do intervalo principal sem Event datado |
| Competições | parcial | universo ainda pequeno para a proposta histórica |
| Mídia da camada editorial | completa | catálogo ainda não possui mídia obrigatória |
| Design | parcialmente evoluído | índice de marcas e catálogo melhorados; jornada integral pendente |
| Documentação de release | desatualizada | relatórios antigos ainda citam 339/364 Entities |

### 2.3 Dívida conhecida

- 516 registros catalográficos ainda sem fonte individual incorporada.
- 34 conceitos, protótipos e one-offs aguardando verificação após R01.
- 482 marcas aguardando decisão e/ou aprofundamento.
- 81 anos entre 1886 e 2026 sem Event canônico datado.
- Pré-história 1769–1885 majoritariamente documental, ainda pouco projetada na timeline.
- Quatro avisos de reconciliação: Bertone, BYD, De Dion-Bouton e Panhard & Levassor.
- Lighthouse e matriz multibrowser ainda não repetidos sobre as atuais 920 Entities.
- Bundle de visualização acima de 500 kB gera aviso não bloqueante.
- Heurist validado em piloto, não novamente exercitado sobre a expansão e suas geometrias.
- Relatório A9.7, status e release manifest narrativo não refletem integralmente MASS01/R01.

---

## 3. Regras invariáveis durante todo o programa

1. O SQLite continua sendo a única autoridade publicada.
2. Toda alteração de dados deve ser reproduzível e preferencialmente idempotente.
3. Nenhum diretório externo cria claim aceito automaticamente.
4. Fonte promocional pode documentar identidade e especificação; prioridade ou influência exige confronto independente.
5. Conflito entre fontes permanece explícito.
6. Nomes iguais não significam identidade igual.
7. Novos predicates e Entity types exigem change control.
8. Toda página pública precisa de narrativa em pt-BR, relações, evidências e mídia adequada.
9. Automóveis de passageiros permanecem no centro da seleção.
10. O build deve continuar funcionando em Node 22 e Python 3.13 com `npm ci`.
11. Nenhum backend, autenticação, banco paralelo ou graph database será introduzido.
12. Um lote não é concluído apenas porque o script executou; é concluído quando o conteúdo publicado foi revisado.

---

## 4. Pipeline padrão e checkpoints de cada lote

Todo lote, independentemente da fase, segue o mesmo fluxo.

| Checkpoint | Nome | Evidência obrigatória | Condição de saída |
|---|---|---|---|
| CP-L0 | Escopo congelado | lista de IDs/candidatos, objetivo, quantidade e exclusões | nenhum item ambíguo no lote |
| CP-L1 | Descoberta | fontes candidatas, identifiers e licença de uso | identidade minimamente reconciliável |
| CP-L2 | Gate de relevância | pontuação por eixos e decisão | cada item em `include`, `context_only`, `hold` ou `exclude` |
| CP-L3 | Pacote de fontes | fonte institucional/primária e fonte independente quando exigida | afirmações centrais sustentáveis |
| CP-L4 | Reconciliação | canonical name, aliases, datas, tipo e external IDs | zero duplicação silenciosa |
| CP-L5 | Modelagem | script idempotente, Entities, statements e qualifiers | SQLite íntegro e determinístico |
| CP-L6 | Claims e evidências | claim/evidence/locator para cada statement importante | cobertura de evidência de 100% |
| CP-L7 | Narrativa | descrição pt-BR contextual e revisão terminológica | mínimo de 30 palavras e contexto histórico claro |
| CP-L8 | Mídia | arquivo local, licença, crédito, alt, dimensões e manifesto | validador de mídia verde |
| CP-L9 | Auditoria editorial | relatório de completude por entidade | todas as incluídas em `complete` |
| CP-L10 | QA de interface | desktop, mobile, teclado, links e estados vazios | nenhuma regressão visual/funcional |
| CP-L11 | Publicação | commit, CI, Pages e smoke test | URL pública confirmada |
| CP-L12 | Encerramento | relatório antes/depois e limitações | lote rastreável e backlog atualizado |

### Regra de bloqueio do lote

Falha em CP-L2, CP-L3, CP-L4, CP-L6 ou CP-L8 impede promoção pública. O registro pode permanecer no registry de candidatos, mas não pode ser apresentado como verbete editorial completo.

---

## 5. Fases do programa de conclusão

## Fase 0 — Rebaseline e governança

**Objetivo:** substituir relatórios defasados por um único snapshot coerente com as 920 Entities.

### Processos

1. Atualizar `CURRENT_STATUS`, relatório A9.7 e handoff mestre.
2. Marcar relatórios de 339/364 Entities como baselines históricos.
3. Gerar dashboard consolidado a partir do SQLite e dos manifestos.
4. Registrar hashes, versões, build, Pagefind, CI, Pages e commit inicial do programa.
5. Congelar este plano como referência de execução.

### Checkpoints

- **CP-0A — Snapshot único:** todas as contagens documentais iguais às contagens do SQLite.
- **CP-0B — Backlog único:** cada Entity e candidato aparece uma única vez com fase, lote, status e prioridade.
- **CP-0C — Governança:** critérios de relevância, completude e publicação aprovados e versionados.

### Gate de saída G0

- Zero relatório ativo contradizendo o snapshot atual.
- Dashboard e backlog reproduzíveis por script.
- Responsabilidade de cada fase identificada no backlog.

---

## Fase 1 — Plataforma de ingestão e simplificação da curadoria

**Objetivo:** transformar pesquisa repetitiva em ingestão assistida, sem terceirizar julgamento histórico.

### Processos

1. Definir schema intermediário `discovery-record`.
2. Criar adapters independentes para fontes com uso permitido:
   - open-vehicle-db;
   - exports próprios/licenciados;
   - APIs contratadas ou autorizadas;
   - snapshots manuais de AllCarIndex, Auto-Data, Carsheet e Ultimatecarpage apenas dentro de seus termos.
3. Implementar cache versionado e checksums.
4. Normalizar marca, modelo, ano, tipo, país e identifiers.
5. Criar reconciliação assistida e relatório de conflitos.
6. Bloquear promoção automática de claims.
7. Registrar proveniência por fonte e campo.

### Checkpoints

- **CP-1A — Contrato:** schema intermediário e validator aprovados.
- **CP-1B — Adapter piloto:** uma fonte aberta percorre importação, normalização e deduplicação.
- **CP-1C — Licenças:** cada adapter possui modo de uso e campos permitidos registrados.
- **CP-1D — Reconciliação:** amostra de 100 registros sem merge incorreto conhecido.
- **CP-1E — Determinismo:** duas execuções produzem snapshots idênticos.

### Gate de saída G1

- Nenhuma fonte é ingerida sem política de licença.
- Todo registro bruto tem origem e checksum.
- Importação em massa não cria statement aceito sem revisão.

---

## Fase 2 — Saneamento, seleção e reconciliação global

**Objetivo:** decidir o destino dos 522 registros catalográficos e resolver a dívida de identidade.

### Processos

1. Aplicar individualmente o gate de relevância às 482 marcas.
2. Confirmar decisões dos 40 veículos especiais.
3. Reconciliar fabricante, organização, grupo e marca.
4. Resolver os quatro avisos canônicos atuais.
5. Classificar cada registro como `include`, `context_only`, `hold` ou `exclude`.
6. Retirar do artefato público candidatos não aprovados.
7. Congelar o universo editorial aprovado para as fases seguintes.

### Checkpoints

- **CP-2A — Marcas M01–M12:** 12/12 ondas com decisão individual documentada.
- **CP-2B — Veículos especiais:** 40/40 decisões confirmadas.
- **CP-2C — Identidade:** zero aviso de canonical name sem decisão registrada.
- **CP-2D — Universo congelado:** total final de Entities públicas e contextuais conhecido.

### Gate de saída G2

- 522/522 registros com decisão editorial explícita.
- Zero candidato público em estado indefinido.
- Zero duplicação crítica ou fusão semântica incorreta.

---

## Fase 3 — Veículos prioritários R02–R07

**Objetivo:** concluir os 34 concepts, protótipos e one-offs restantes após o R01.

### Lotes previstos

| Lote | Escopo | Meta aproximada |
|---|---|---:|
| R02 | recordistas e programas experimentais | 6 |
| R03 | segurança, eficiência e energia | 6 |
| R04 | arquitetura, embalagem e novos segmentos | 6 |
| R05 | aerodinâmica e linguagem de design | 6 |
| R06 | one-offs e tradição de carrozzeria | 5 |
| R07 | remanescentes, conflitos e revisão cruzada | 5 |

### Checkpoints

- **CP-3A:** R02–R04 publicados e auditados.
- **CP-3B:** R05–R07 publicados e auditados.
- **CP-3C:** 40/40 veículos especiais decididos; todos os incluídos completos.

### Gate de saída G3

- Zero veículo especial público somente catalográfico.
- Todos os incluídos com duas fontes quando houver alegação de influência.
- Todas as relações de marca e tecnologia evidenciadas.
- Mídia local e licenciada para todos os promovidos.

---

## Fase 4 — Histórias de marcas B01–B12

**Objetivo:** permitir que cada marca aprovada conte sua trajetória e se conecte à rede industrial.

### Organização dos lotes

As ondas B01–B12 herdam os clusters M01–M12, mas processam apenas as marcas aprovadas em G2.

### Conteúdo mínimo por marca

1. origem, fundação e local;
2. fundadores ou organização responsável;
3. períodos de atividade e mudanças de nome;
4. antecessoras, sucessoras, fusões e aquisições;
5. grupo controlador por período, quando aplicável;
6. modelos historicamente relevantes;
7. tecnologias, design ou competição associados;
8. encerramento, dormência ou renascimento;
9. fontes institucionais e independentes;
10. narrativa cronológica e mídia.

### Checkpoints

- **CP-4A:** B01–B03 completos.
- **CP-4B:** B04–B06 completos.
- **CP-4C:** B07–B09 completos.
- **CP-4D:** B10–B12 completos.
- **CP-4E — Rede industrial:** todas as marcas ativas, extintas ou fundidas conectadas a pelo menos um ponto histórico relevante.

### Gate de saída G4

- 100% das marcas públicas em `complete`.
- Toda marca possui ao menos três statements evidenciados e uma trajetória temporal.
- Toda fusão, aquisição, sucessão ou revival possui validade temporal quando conhecida.
- Nenhuma página de marca pública é apenas um cartão nominal.

---

## Fase 5 — Cronologia integral 1769–2026

**Objetivo:** fazer cada ano contar uma história e incorporar os fundamentos anteriores a 1886.

### Subfase F5A — Fundamentos 1769–1885

Converter o documento de fundamentos em Events, pessoas, veículos, tecnologias e claims canônicos. Cobrir vapor, combustão interna, direção, frenagem, motores estacionários e circulação experimental sem exigir um evento artificial para cada ano.

### Subfase F5B — Registro anual 1886–2026

Cada ano deve possuir:

- uma síntese editorial em pt-BR;
- pelo menos um marco evidenciado ou uma explicação documentada de continuidade/transição;
- conexões com Entities centrais;
- fontes e precisão temporal;
- caminho de descoberta para o ano anterior e posterior.

### Ondas cronológicas

| Lote | Intervalo |
|---|---|
| Y01 | 1886–1900 |
| Y02 | 1901–1918 |
| Y03 | 1919–1939 |
| Y04 | 1940–1959 |
| Y05 | 1960–1979 |
| Y06 | 1980–1999 |
| Y07 | 2000–2009 |
| Y08 | 2010–2019 |
| Y09 | 2020–2026 e revisão transversal |

### Checkpoints

- **CP-5A:** fundamentos 1769–1885 publicados e conectados.
- **CP-5B:** Y01–Y03 completos.
- **CP-5C:** Y04–Y06 completos.
- **CP-5D:** Y07–Y09 completos.
- **CP-5E — Cobertura anual:** 141/141 anos com narrativa e pelo menos um marco/contexto evidenciado.

### Gate de saída G5

- Nenhum ano de 1886–2026 sem página ou narrativa.
- Datas parciais e fatos futuros distinguem precisão e realização.
- Timeline, páginas anuais e busca refletem o mesmo SQLite.
- Transições entre anos formam uma narrativa contínua, não uma lista isolada.

---

## Fase 6 — Automóveis de passageiros e genealogias de modelos

**Objetivo:** completar o eixo central do Atlas com os automóveis que passaram pelo gate histórico.

### Processos

1. Consolidar candidatos por era, região e contribuição.
2. Separar família, geração, variante, configuração e standalone conforme o modelo congelado.
3. Evitar uma Entity por trim ou ano-modelo sem necessidade histórica.
4. Conectar origem, sucessão, plataforma, produção, design, tecnologia e mercado.
5. Incluir conceitos somente quando tiverem trajetória histórica própria.
6. Cobrir automóveis populares, luxo, esportivos, utilitários de passageiros e novos segmentos sem viés apenas europeu/norte-americano.

### Lotes

- **V01:** pioneiros e industrialização.
- **V02:** entre-guerras e consolidação de arquiteturas.
- **V03:** reconstrução e motorização de massa.
- **V04:** esportivos, GT e performance.
- **V05:** compactos, familiares e novos segmentos.
- **V06:** segurança, emissões e crises energéticas.
- **V07:** globalização e plataformas compartilhadas.
- **V08:** híbridos, elétricos e software.
- **V09:** revisão regional e lacunas.

### Checkpoints

- **CP-6A:** V01–V03 completos.
- **CP-6B:** V04–V06 completos.
- **CP-6C:** V07–V09 completos.
- **CP-6D — Genealogia:** toda família aprovada possui predecessor/sucessor ou justificativa de isolamento.

### Gate de saída G6

- 100% dos veículos públicos em `complete`.
- Nenhuma duplicação entre família, geração e variante.
- Veículos centrais têm quatro ou mais statements evidenciados.
- Cobertura regional e temporal auditada contra o universo aprovado.

---

## Fase 7 — Genealogias tecnológicas

**Objetivo:** explicar como tecnologias surgiram, foram testadas, transferidas e difundidas.

### Trilhas

| Lote | Trilha |
|---|---|
| T01 | vapor, combustão e combustíveis |
| T02 | arquitetura de motores e alimentação |
| T03 | transmissão, tração e chassi |
| T04 | carroceria, materiais e produção |
| T05 | aerodinâmica e desempenho |
| T06 | segurança passiva e ativa |
| T07 | emissões, eficiência, híbridos e elétricos |
| T08 | eletrônica, software, assistência e automação |

### Checkpoints

- **CP-7A:** T01–T04 completos.
- **CP-7B:** T05–T08 completos.
- **CP-7C — Transferência:** toda tecnologia possui origem, aplicação e difusão ou limitação documentada.

### Gate de saída G7

- 100% das tecnologias públicas completas.
- Prioridade, invenção e popularização não são tratadas como sinônimos.
- Relações com veículos, pessoas, fornecedores e regulações possuem evidência.

---

## Fase 8 — Competições e transferência para automóveis de rua

**Objetivo:** ampliar Motorsport como laboratório histórico conectado ao produto principal.

### Trilhas

- **C01:** corridas urbanas, provas de cidade a cidade e primeiros GPs.
- **C02:** Le Mans e endurance.
- **C03:** Grand Prix e Fórmula 1.
- **C04:** rally, WRC e Grupo B.
- **C05:** carros esporte, Grupo C e GT.
- **C06:** Indianapolis, NASCAR e tradições norte-americanas.
- **C07:** turismo e campeonatos regionais relevantes.
- **C08:** eletrificação, eficiência e competições contemporâneas.

### Modelagem mínima

Competition → Season → Event → Entry → Vehicle/VehicleInstance → Team → Driver → CircuitLayout.

### Checkpoints

- **CP-8A:** C01–C04 completos.
- **CP-8B:** C05–C08 completos.
- **CP-8C — Transferência:** cada trilha possui exemplos evidenciados de influência sobre automóveis/tecnologias ou uma delimitação explícita.

### Gate de saída G8

- Competições aprovadas possuem estrutura temporal navegável.
- Resultados usados em narrativa têm Entry e fonte.
- CircuitLayout, não Circuit global, recebe comprimento/configuração.
- O Atlas não tenta se tornar banco exaustivo de resultados esportivos.

---

## Fase 9 — Geografia, fornecedores e legislação contextual

**Objetivo:** completar contexto industrial sem deslocar o foco dos automóveis.

### Processos

1. Expandir lugares e instalações necessários às histórias aprovadas.
2. Registrar precisão, fonte e revisão de toda geometria.
3. Incluir fornecedores apenas quando explicarem tecnologia, produção ou cadeia industrial relevante.
4. Incluir caminhões, ônibus e motocicletas apenas como entidades contextuais indispensáveis ou citações.
5. Modelar regulações de segurança, emissões, competição e mercado quando alterarem diretamente o automóvel.
6. Proibir geocoding em runtime.

### Checkpoints

- **CP-9A — Geografia:** todos os lugares publicados têm fonte e precisão.
- **CP-9B — Fornecedores:** cada fornecedor público está ligado a contribuição histórica explícita.
- **CP-9C — Legislação:** toda regulação publicada tem jurisdição, vigência, fonte e efeito.
- **CP-9D — Escopo adjacente:** zero expansão lateral sem conexão com automóveis de passageiros.

### Gate de saída G9

- 100% das geometrias `release_ready`.
- Mapa tem créditos, alternativas textuais e nenhum ponto protótipo.
- Entidades adjacentes não superam ou diluem o foco principal.

---

## Fase 10 — Acervo visual integral

**Objetivo:** obter cobertura visual juridicamente segura e editorialmente honesta para todo o universo público final.

### Hierarquia de preferência

1. domínio público;
2. CC0;
3. CC BY;
4. CC BY-SA preservando a licença;
5. autorização institucional;
6. ilustração original claramente identificada.

### Processos

1. Validar licença antes do download.
2. Armazenar arquivo local sem hotlink.
3. Otimizar formatos e miniaturas.
4. Registrar autoria, origem, licença, URL, crédito, alt e data.
5. Diferenciar documento histórico de representação interpretativa.
6. Revisar alt text por função editorial, não apenas aparência.

### Checkpoints

- **CP-10A:** 25% do universo final coberto e auditado.
- **CP-10B:** 50% coberto.
- **CP-10C:** 75% coberto.
- **CP-10D:** 100% coberto.
- **CP-10E — Auditoria jurídica:** zero licença ausente, incompatível ou reclassificada.

### Gate de saída G10

- Cobertura de mídia 100%/100% das Entities públicas.
- Zero hotlink externo.
- Zero mídia sem alt, crédito ou licença.
- Dimensões explícitas e formatos web eficientes.

---

## Fase 11 — Produto editorial e navegação UX2

**Objetivo:** transformar o banco completo em uma experiência coerente de arquivo/museu contemporâneo.

### Entregas

1. **Início:** percursos, eras, temas e descobertas editoriais.
2. **Página de marca:** narrativa, timeline, genealogia corporativa, modelos, pessoas, competição e tecnologias.
3. **Página anual:** síntese, marcos, contexto e navegação anterior/próximo.
4. **Página de veículo:** narrativa antes de metadados, genealogia, tecnologia, competição e evidência.
5. **Página de tecnologia:** origem, adoção, difusão e veículos relacionados.
6. **Página de competição:** temporadas, eventos, entries e transferência tecnológica.
7. **Página de fonte:** referência, cobertura e statements sustentados.
8. **Índices:** veículos, marcas, anos, tecnologias, competições, pessoas e lugares.
9. **Filtros:** período, região, tipo, estado editorial e contribuição histórica.
10. **Visualizações:** grafo, timeline, mapa e comparação com alternativa textual equivalente.

### Checkpoints

- **CP-11A — Arquitetura de informação:** mapa de navegação e templates aprovados.
- **CP-11B — Sistema visual:** tokens, componentes, estados e responsividade aprovados.
- **CP-11C — Templates:** todos os tipos principais implementados.
- **CP-11D — Percursos:** seis percursos históricos e seis novos percursos de expansão aprovados.
- **CP-11E — Mobile:** nenhuma função central depende de viewport desktop.

### Gate de saída G11

- Usuário consegue partir de qualquer marca, ano ou veículo e alcançar relações relevantes.
- Metadados técnicos não antecedem a narrativa principal.
- Nenhuma visualização é a única forma de acessar informação.
- Estados vazios, loading e erro são claros.
- Inserção de conteúdo não usa `innerHTML` inseguro.

---

## Fase 12 — Qualidade editorial, acessibilidade e performance

**Objetivo:** provar que conteúdo e produto completo mantêm qualidade em escala.

### Auditorias

1. completude editorial;
2. integridade de claims/evidence;
3. links e URLs sob `/atlas/`;
4. busca por nomes, aliases, acentos, tipos e períodos;
5. WCAG 2.2 AA;
6. teclado e foco;
7. contraste e redução de movimento;
8. Lighthouse;
9. Chrome, Firefox e Safari/WebKit;
10. desktop e mobile;
11. performance de build e tamanho de bundles;
12. exportação determinística;
13. varredura de segredos e licenças.

### Checkpoints

- **CP-12A — Dados:** zero erro, warning crítico ou Entity pública incompleta.
- **CP-12B — Acessibilidade:** WCAG 2.2 AA e Lighthouse Accessibility 100 nos templates críticos.
- **CP-12C — Navegadores:** matriz Chrome/Firefox/WebKit verde.
- **CP-12D — Performance:** Lighthouse Performance ≥ 90 nos percursos definidos e aviso de bundle resolvido ou formalmente justificado.
- **CP-12E — Segurança/licenças:** zero segredo, dependência crítica ou incompatibilidade jurídica.
- **CP-12F — Determinismo:** segundo build sem alteração não muda artefatos determinísticos.

### Gate de saída G12

- Todos os checkpoints CP-12 verdes.
- Nenhuma exceção silenciosa.
- Qualquer limitação residual é explicitamente não crítica e registrada.

---

## Fase 13 — Round-trip, release e encerramento

**Objetivo:** fechar o ciclo operacional e publicar a versão final do programa.

### Processos

1. Reexecutar `Zotero/OpenRefine/Heurist → SQLite → validação → build → página`.
2. Incluir geometrias no piloto Heurist para tentar 10/10.
3. Atualizar relatório consolidado com contagens e hashes finais.
4. Congelar manifests e checksums.
5. Executar CI e Pages no commit candidato.
6. Fazer smoke test de home, busca, sitemap, índices e amostra estratificada de Entities.
7. Criar tag anotada e GitHub Release.
8. Atualizar handoff, status e política de manutenção.

### Checkpoints

- **CP-13A — Round-trip:** sem perda semântica crítica e mapa Heurist exercitado.
- **CP-13B — Release candidate:** todos os gates G0–G12 registrados como verdes.
- **CP-13C — Deploy:** URL pública, assets e Pagefind confirmados.
- **CP-13D — Release:** tag, release, checksums e limitações publicados.
- **CP-13E — Handoff:** backlog de conclusão zerado e manutenção futura separada do escopo concluído.

### Gate final GF

O Atlas somente recebe o estado **100% CONCLUÍDO NO ESCOPO** quando:

- [ ] G0–G12 estão verdes;
- [ ] 100% das Entities públicas estão `complete`;
- [ ] zero Entity pública permanece apenas `catalog`;
- [ ] zero claim histórico importante está sem evidence;
- [ ] 141/141 anos de 1886–2026 contam uma história;
- [ ] fundamentos 1769–1885 estão publicados;
- [ ] 100% das marcas aprovadas possuem história conectada;
- [ ] 100% das mídias estão válidas;
- [ ] todas as experiências e índices estão navegáveis;
- [ ] WCAG, Lighthouse e navegadores estão aprovados;
- [ ] CI, Pages e smoke test público estão verdes;
- [ ] relatório, tag, release e handoff correspondem ao mesmo commit;
- [ ] não há hard gate, backlog crítico ou decisão editorial pendente.

---

## 6. Marcos executivos

| Marco | Fases | Resultado acumulado |
|---|---|---|
| M0 — Controle | 0 | baseline e backlog únicos |
| M1 — Curadoria escalável | 1–2 | ingestão assistida e universo aprovado |
| M2 — Catálogo resolvido | 3–4 | veículos especiais e marcas concluídos |
| M3 — História contínua | 5–6 | todos os anos e veículos centrais conectados |
| M4 — Rede explicativa | 7–9 | tecnologia, competição, geografia e contexto completos |
| M5 — Museu digital | 10–11 | mídia integral e UX editorial final |
| M6 — Prova de qualidade | 12 | QA integral em escala |
| M7 — Produto final | 13 | round-trip, deploy, tag e release final |

Nenhum marco pode ser declarado concluído se um gate de fase incluída estiver vermelho.

---

## 7. Dashboard obrigatório de acompanhamento

O status deve ser regenerado após cada lote e conter:

| Indicador | Baseline | Meta final |
|---|---:|---:|
| Candidates com decisão | parcial | 100% |
| Entities públicas catalog-only | 522 | 0 |
| Entities públicas completas | 146 | 100% |
| Statements importantes com evidence | validado no corpus atual | 100% |
| Marcas públicas completas | 4 | 100% das aprovadas |
| Veículos públicos completos | 45 | 100% dos aprovados |
| Anos 1886–2026 narrados | 60/141 com Event | 141/141 com narrativa |
| Fundamentos 1769–1885 | parcial | conjunto aprovado completo |
| Mídia válida | 398 obrigatórias | 100% do universo final |
| Geometrias válidas | 4/4 atuais | 100% das publicadas |
| Testes | 12 | todos verdes |
| Avisos de reconciliação | 4 | 0 sem decisão |
| Lighthouse atual | baseline antigo | metas CP-12B/CP-12D |
| Heurist | 9/10 piloto | 10/10 ou limitação não crítica aprovada |

### Semáforo

- **Verde:** checkpoint possui evidência e critério atendido.
- **Amarelo:** trabalho em curso, sem quebra do baseline.
- **Vermelho:** gate bloqueado, regressão ou evidência insuficiente.
- **Cinza:** fase ainda não iniciada.

Percentual de conclusão nunca será calculado apenas pela quantidade de páginas. Deve ponderar decisão editorial, completude, evidência, mídia e QA.

---

## 8. Cadência operacional

### Por lote

1. abrir escopo CP-L0;
2. pesquisar e decidir CP-L1–L3;
3. reconciliar e modelar CP-L4–L6;
4. narrar e cobrir mídia CP-L7–L8;
5. auditar CP-L9–L10;
6. publicar e encerrar CP-L11–L12.

### Por marco

1. congelar contagens;
2. gerar auditoria editorial;
3. executar `npm run verify`;
4. executar auditoria de links;
5. revisar desktop/mobile;
6. registrar CI, Pages, hash e URL;
7. aprovar ou bloquear o marco.

### Artefatos mínimos por lote

- script idempotente;
- snapshot ou registry de entrada;
- relatório de fontes e decisões;
- diff de contagens;
- resultado dos validadores;
- páginas amostrais revisadas;
- commit e workflow;
- atualização do dashboard.

---

## 9. Riscos e controles

| Risco | Controle |
|---|---|
| Curadoria infinita | universo congelado em G2 e change control posterior |
| Copiar diretórios externos | adapters limitados por licença e sem promoção automática |
| Quantidade sem profundidade | meta baseada em `complete`, não em número de páginas |
| Viés regional | auditoria por era, região e contribuição em G6 |
| Afirmações promocionais | segunda fonte para prioridade e influência |
| Mídia sem licença | gate G10 bloqueante |
| Marca confundida com empresa | reconciliação e validade temporal em G2/G4 |
| Timeline artificial | contexto documentado, precisão e continuidade em G5 |
| Motorsport dominar o escopo | seleção por transferência e relevância em G8 |
| UX desconexa | arquitetura de informação e percursos bloqueantes em G11 |
| Regressão por escala | QA completo e performance em G12 |
| Documentação defasada | dashboard regenerado a cada lote e release |

---

## 10. Próxima ação autorizável

A execução deve começar pela **Fase 0**, seguida da **Fase 1**. O conteúdo R02 pode avançar em paralelo somente depois de o backlog único de G0 identificar formalmente seus registros. A primeira entrega concreta será:

1. script de dashboard/rebaseline;
2. atualização dos documentos ativos;
3. backlog unificado com 920 Entities e 522 decisões pendentes;
4. contrato `discovery-record`;
5. adapter piloto de fonte aberta;
6. abertura formal do lote R02.

Este documento substitui roadmaps antigos como plano operacional corrente. Documentos anteriores continuam como rastreabilidade dos baselines e lotes já executados.
