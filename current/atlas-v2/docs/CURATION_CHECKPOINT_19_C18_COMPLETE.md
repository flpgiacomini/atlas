# CP19 — C18: auditoria semântica transversal completa

Data de verificação: 2026-08-25

## Resultado

O C18 auditou **522/522** decisões canônicas e encerrou com **522 PASS, zero
FAIL**. O artefato `content/c18-semantic-audit.json` registra, item a item,
identidade, evidência, escopo narrativo permitido, temporalidade, genealogia,
região e estado de publicação. O relatório compacto está em
`reports/c18-semantic-audit.json` e sua reprodução é bloqueante no CI.

## Checkpoints encerrados

1. **C18.1 — Identidades e aliases: PASS.** Os 522 IDs resolvem para entidade
   canônica e identidade legada, sem colisão normalizada. Aliases vazios são
   tratados como ausência de alias conhecido, não como falha; alias duplicado
   ou idêntico ao nome canônico passa a falhar no CI.
2. **C18.2 — Retenções: PASS.** As 51 retenções foram reclassificadas por
   alcance probatório. Nove têm fonte individual e 42 preservam somente a
   identidade legada após busca negativa. Estas 42 estão explicitamente
   impedidas de publicar claims; retenção não é apresentada como inexistência.
3. **C18.3 — Promoções: PASS.** As 471 promoções têm fonte resolvida, decisão,
   rationale e no mínimo duas assertions localizadas. Promoção passa a
   significar elegibilidade editorial, não autorização para inventar biografia.
4. **C18.4 — Genealogia: PASS.** Há 17 relações documentadas entre 23
   participantes. Para os demais registros o estado é `not-asserted`, jamais
   “sem relação”; nenhuma genealogia é inferida a partir de nome ou catálogo.
5. **C18.5 — Cronologia: PASS.** 78 marcos cobrem 61 marcas. Ausência de marco
   é registrada como `not-asserted`; datas não são derivadas de snippets ou
   categorias.
6. **C18.6 — Narrativa e fontes: PASS.** O C18 separa quatro níveis: 15 itens
   `claim-backed`, 54 `assertion-backed`, 411 `identity-only` e 42
   `catalog-only-no-public-claims`. Cada nível possui permissão pública
   explícita e verificável.
7. **C18.7 — Cobertura regional: PASS.** As 482 marcas possuem onda e região;
   o relatório apresenta a distribuição pelas doze regiões editoriais.
8. **C18.8 — Escopo: PASS.** As 482 marcas e 40 veículos mantêm seus tipos.
   Caminhões, ônibus, motocicletas e fornecedores não são promovidos além do
   papel contextual permitido pelo recorte.
9. **C18.9 — Fechamento técnico: PASS.** O gerador é determinístico, possui
   modo `--check`, hash canônico e foi incorporado ao workflow raiz.

## Leitura correta dos números

O C18 encerra a **curadoria de entrada e seus limites semânticos**. Ele não
afirma que 482 marcas possuem genealogia profunda nem que 411 identidades de
catálogo já possuem biografia publicável. Pelo contrário: o novo contrato
impede essa extrapolação. A expansão narrativa, visual e das relações acontece
no CP20 somente quando houver evidência própria.

Checkpoint C18: **PASS**. Checkpoint CP19: **PASS e semanticamente congelado**.
