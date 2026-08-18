# Roadmap de enriquecimento editorial do Atlas

Baseline: 18 de agosto de 2026  
Banco canônico: `current/atlas-web/data/atlas.sqlite`  
Inventário operacional: `handoff/EDITORIAL_COMPLETENESS_BACKLOG.csv`

## Objetivo

Elevar as 339 entidades do Atlas ao piso de completude definido em
`current/atlas-web/data/editorial-completeness.criteria.json`, preservando o contrato
SQLite → validação → exportação → Astro → Pagefind. “Completa” significa completa no
contexto editorial do Atlas, não um catálogo universal de versões, peças ou resultados.

## Estado de partida

| Situação | Entidades |
|---|---:|
| Completas | 6 |
| Substanciais | 3 |
| Parciais | 165 |
| Esboços | 165 |
| Total | 339 |

Os lotes E01 e E02 já promoveram nove entidades para completa ou substancial. As 330
entidades ainda abaixo desse patamar estão distribuídas entre E03 e E21. O Benz Patent
Motor Car, já narrado em E02, é o único carry-over explícito: volta em E09 para receber
as relações estruturadas que ainda faltam.

## Definição de pronto para cada entidade

Uma entidade só sai do lote quando:

1. possui descrição contextual em pt-BR com pelo menos 30 palavras;
2. alcança o número mínimo de statements definido para seu tipo;
3. todos os statements editoriais importantes possuem claim e evidence;
4. fonte, autoria, editora, URL, data de publicação e acesso são preenchidos quando disponíveis;
5. datas parciais declaram sua precisão e conflitos não são silenciosamente resolvidos;
6. metadados obrigatórios do tipo estão preenchidos;
7. a página gerada, busca e relações foram verificadas;
8. a auditoria classifica a entidade como `complete` ou `substantial`, sem lacuna crítica registrada.

## Sequência dos lotes

| Lote | Escopo congelado | Qtde. | Estado | Resultado principal |
|---|---|---:|---|---|
| E01 | Carl Benz, Henry Ford, Richard Attwood, Nils Bohlin e Ferdinand Alexander Porsche | 5 | concluído | Biografias, datas vitais, vínculos profissionais e evidências institucionais |
| E02 | Benz Patent Motor Car, Ford Model T, Porsche 911, Porsche 917 e Volvo PV544 | 5 | concluído | Narrativas dos percursos centrais; quatro entidades promovidas |
| E03 | Pessoas, faixa alfabética `Alec Issigonis`–`Georges Bouton` | 10 | pendente | Pioneiros, projetistas e fundadores |
| E04 | Pessoas, faixa `Gioacchino Colombo`–`Kiichiro Toyoda` | 10 | pendente | Engenharia, indústria e design |
| E05 | Pessoas, faixa `Kurt Ahrens Jr.`–`Wilhelm Werner` | 10 | pendente | Competição, segurança e liderança técnica |
| E06 | Todas as marcas ainda pendentes | 18 | pendente | Origem, identidade, proprietários e continuidade histórica |
| E07 | Organizações, faixa `Benz & Cie.`–`Hyundai Motor Company` | 15 | pendente | Fundação, localização, liderança e sucessões |
| E08 | Organizações, faixa `Lancia & C.`–`Volvo Cars` | 15 | pendente | Estrutura corporativa, produção e transições |
| E09 | Veículos, faixa `Audi quattro`–`Ford Mustang` | 20 | pendente | Contexto histórico, fabricação, tecnologia e genealogia |
| E10 | Veículos, faixa `Ford Quadricycle`–`Panhard-Levassor Type M2E` | 20 | pendente | Pioneirismo, escala industrial e arquiteturas iniciais |
| E11 | Veículos, faixa `Peugeot Type 1`–`Renault Espace — First Generation` | 20 | pendente | Reconstrução, desempenho, utilidade e novos segmentos |
| E12 | Veículos, faixa `Renault Type A`–`ŠKODA 1000 MB` | 18 | pendente | Produção global, segurança e propulsões alternativas |
| E13 | Todas as tecnologias ainda pendentes | 24 | pendente | Definição, autoria, aplicação, popularização e impacto |
| E14 | Todos os componentes ainda pendentes | 7 | pendente | Função técnica, desenvolvimento e veículos relacionados |
| E15 | Eventos, faixa `1903 Cadillac Runabout production`–`End of BR-800 production` | 26 | pendente | Cronologia documentada e participantes |
| E16 | Eventos, faixa `End of Ford Model T production`–`Hyundai Pony market introduction` | 26 | pendente | Industrialização, produção e expansão internacional |
| E17 | Eventos, faixa `Introduction of turbocharger in Porsche 911`–`Presentation of first Porsche 911 Targa` | 26 | pendente | Tecnologia, lançamentos, regulação e competição |
| E18 | Eventos, faixa `Presentation of Porsche 911 Type 992`–`ŠKODA 1000 MB production start` | 25 | pendente | Marcos recentes, segurança e transições tecnológicas |
| E19 | Todas as instalações e lugares pendentes | 14 | pendente | Função industrial, localização, período e precisão geográfica |
| E20 | Circuitos, layouts, competições e equipes pendentes | 17 | pendente | Infraestrutura esportiva, governança, traçados e relações temporais |
| E21 | Entries e VehicleInstances pendentes | 9 | pendente | Chassi, configuração, equipe, pilotos, evento, número e resultado |

## Contabilidade de cobertura pendente

| Tipos | Entidades | Lotes |
|---|---:|---|
| Person | 30 | E03–E05 |
| Brand | 18 | E06 |
| Organization | 30 | E07–E08 |
| Vehicle | 78 | E09–E12 |
| Technology | 24 | E13 |
| Component | 7 | E14 |
| Event | 103 | E15–E18 |
| Facility + Place | 14 | E19 |
| Circuit + CircuitLayout + Competition + Team | 17 | E20 |
| Entry + VehicleInstance | 9 | E21 |
| **Total pendente** | **330** | **E03–E21** |

## Método de execução de cada lote

### 1. Pesquisa

- começar por arquivos públicos, fabricantes, museus, órgãos governamentais e acervos institucionais;
- confrontar fontes independentes quando a afirmação for disputada ou promocional;
- registrar lacuna ou conflito em vez de completar por inferência;
- não usar texto gerado automaticamente como fonte histórica.

### 2. Modelagem

- atualizar o SQLite exclusivamente por script idempotente versionado;
- reutilizar entidades, fontes e predicados existentes antes de criar novos registros;
- submeter predicados novos à regra formal de change control;
- criar claim/evidence para cada statement novo.

### 3. Controle de qualidade

Executar, no mínimo:

```powershell
python ../canonical-model/scripts/validate_atlas_db.py data/atlas.sqlite
python scripts/audit_editorial_completeness.py
python -m unittest discover -s tests -v
npm.cmd run build
```

Além dos checks automáticos, revisar uma página desktop e uma móvel de cada tipo alterado.

### 4. Publicação

- um commit de conteúdo por lote;
- push somente após validação verde;
- registrar contagens antes/depois no relatório de completude;
- confirmar o workflow de Pages e fazer smoke test da URL pública.

## Marcos de acompanhamento

| Marco | Lotes incluídos | Meta acumulada |
|---|---|---:|
| M1 — Pessoas e instituições | E01–E08 | 88 entidades únicas tratadas |
| M2 — Veículos | E09–E12 | 165 entidades únicas acumuladas |
| M3 — Engenharia | E13–E14 | 196 entidades únicas acumuladas |
| M4 — Cronologia | E15–E18 | 299 entidades únicas acumuladas |
| M5 — Geografia e competição | E19–E21 | 339 entidades cobertas |

As metas de marco medem cobertura de execução. O encerramento exige também que a auditoria
final não apresente entidades `stub`, lacunas críticas de evidência ou falhas de validação.

## Gate final editorial

O enriquecimento somente será considerado concluído quando:

- 339/339 entidades tiverem sido processadas por um lote;
- nenhuma entidade permanecer como `stub`;
- toda entidade abaixo de `substantial` possuir uma limitação explícita e justificada;
- fontes institucionais ou bibliográficas sustentarem as afirmações centrais;
- o banco, exportação, testes, build e Pagefind estiverem verdes;
- os seis percursos obrigatórios forem novamente verificados em desktop e mobile;
- o relatório A9.7 registrar contagens finais, hash do banco, commit e URL implantada.

## Limites declarados

Este roadmap não promete cada acabamento, versão, VIN, peça, volta ou resultado esportivo.
Ele promete uma página historicamente contextualizada, navegável e sustentada por evidências
para cada entidade que já integra o escopo canônico do Atlas.
