# CP19 — Lote C01: candidatos históricos já apoiados por fonte

## Resultado

Os seis candidatos que entraram no CP19 com fonte individual e evidência mínima
foram revisados e promovidos ao nível editorial:

1. Aston Martin Bulldog;
2. Chrysler Turbine Car;
3. Ferrari P4/5 by Pininfarina;
4. Maybach Exelero;
5. Mercedes-Benz C 111;
6. Volkswagen W12.

A decisão não decorre apenas de fama ou raridade. Cada pacote registra a função
histórica, a fonte institucional ou participante, ao menos duas afirmações
recuperáveis, localizador, justificativa e data de revisão.

## Fontes e limites

- **Bulldog:** Aston Martin Heritage Trust; a passagem por 205,4 mph é tratada
  como demonstração do protótipo restaurado, não como recorde de produção;
- **Turbine Car:** Smithsonian; o programa de 50 automóveis, as carrocerias Ghia
  e as limitações de uso são preservados sem transformar teste em produção;
- **P4/5:** publicação do responsável por projetos especiais; a encomenda, a
  homenagem à série P e os componentes exclusivos são atribuídos ao projeto;
- **Exelero:** arquivo corporativo Fulda; o veículo é tratado como demonstrador
  de pneus e comunicação, com desempenho documentado;
- **C 111:** Mercedes-Benz Classic; o programa experimental, Wankel, materiais e
  derivações de recorde permanecem distintos de um modelo de produção;
- **W12:** Volkswagen Classic; arquitetura e recordes de duração são tratados
  como programa técnico, sem inferir continuidade direta para todo modelo W12.

Uma fonte confiável pode sustentar uma afirmação conforme o contrato v2. Isso
não elimina a exibição do nível de corroboração nem autoriza extrapolações.

## Implementação

- `content/canonical-curation-reviews.json`: pacotes de revisão versionados;
- `scripts/audit_canonical_curation.py`: valida decisão, fontes, afirmações,
  identidade, estado editorial e ausência de revisão órfã;
- `current/atlas-web/scripts/promote_catalog_c01.py`: promoção reproduzível no
  banco canônico legado durante a transição;
- migração JSON-LD, checksums e bundles regenerados deterministicamente.

## Métricas

- resolvidos neste lote: **6**;
- resolvidos no CP19: **6/522**;
- pendentes: **516**;
- candidatos históricos pendentes: **34**;
- marcas pendentes: **482**;
- colisões ou entidades ausentes: **0**.

O próximo lote é o **C02**, iniciando os 34 candidatos históricos sem fonte
individual, priorizados por antiguidade e influência documentável.
