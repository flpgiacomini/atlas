# CP19 — Inventário de curadoria canônica

## Reconciliação do escopo

O número **522** não representa todos os registros avaliados no legado. Ele é a
fila formada exclusivamente pelos candidatos cuja decisão anterior era
`cataloged`:

- **482 marcas** do censo M01–M12;
- **40 conceitos, protótipos, programas experimentais e one-offs**;
- total: **522 registros catalográficos a resolver**.

As duas fontes de entrada contêm **558 registros**. Os 36 restantes já possuem
decisão terminal preservada: 33 `published`, dois `context_only` e um `hold`.
O inventário não promove nem rebaixa silenciosamente nenhuma dessas decisões.

## Estado inicial do CP19

- identidades legadas duplicadas: **0**;
- entidades migradas ausentes: **0**;
- fila com fonte e evidência individual: **6**;
- fila ainda limitada à identidade catalográfica: **516**;
- marcas ainda limitadas à identidade catalográfica: **482**;
- candidatos históricos ainda sem fonte individual suficiente: **34**.

Os seis registros já apoiados por fonte são Aston Martin Bulldog, Chrysler
Turbine Car, Ferrari P4/5 by Pininfarina, Maybach Exelero, Mercedes-Benz C 111 e
Volkswagen W12. Eles estão **prontos para revisão editorial**, não promovidos
automaticamente: uma única relação de atribuição ainda não basta para sustentar
toda a narrativa histórica do veículo.

## Contrato implementado

O arquivo `content/canonical-curation-decisions.json` passa a ser a fila
versionada do CP19. O script `scripts/audit_canonical_curation.py` reconcilia os
CSVs legados com os IDs semânticos da v2 e bloqueia:

- alteração silenciosa da contagem de 522;
- colisão de identidade legada;
- candidato com UUID sem entidade migrada correspondente;
- relatório ou decisões desatualizados;
- promoção implícita de `context_only` ou `hold`.

## Próximos lotes

1. **C01 — seis candidatos históricos já apoiados por fonte:** ampliar claims,
   revisar a contribuição e decidir promoção ou permanência no catálogo;
2. **C02–C05 — 34 candidatos históricos restantes:** pesquisar por período,
   com fonte individual e evidência recuperável;
3. **C06–C17 — 482 marcas:** processar as ondas M01–M12, registrando fundação,
   encerramento, sucessão e relações corporativas apenas quando evidenciadas;
4. **C18 — auditoria transversal:** duplicatas semânticas, conflitos, aliases,
   relações e correspondência narrativa–fonte.

O checkpoint termina somente com **522/522 decisões explícitas**, sem tratar
“registro pesquisável” como sinônimo de “história editorial concluída”.
