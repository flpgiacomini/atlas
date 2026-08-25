# CP19 — C06 completo: onda M01

Data de verificação: 2026-08-25

## Escopo encerrado

O C06 resolveu integralmente a onda M01, dedicada às linhagens pioneiras e à
primeira industrialização do automóvel. O universo auditado contém **41 marcas**:
**29 candidatos da fila CP19** e **12 registros que já possuíam decisão legada
`published`**.

Os 29 candidatos receberam fonte individual, descrição revisada, decisão
explícita, pacote de revisão canônico e marco na visualização temporal de marcas.
As 12 marcas publicadas foram verificadas contra a mesma visualização; lacunas de
cobertura foram preenchidas sem reabrir suas decisões legadas.

## Resultado das decisões

- candidatos resolvidos no C06: **29/29**;
- promovidos para o corte editorial v2: **27**;
- retidos no catálogo após revisão: **2** — Peerless e REO;
- marcas M01 cobertas na timeline genealógica: **41/41**;
- fontes canônicas após o lote: **225**;
- perdas, colisões de identidade ou revisões órfãs: **0**.

Peerless e REO permanecem pesquisáveis e preservadas no catálogo. A retenção não
é descarte: registra que as fontes institucionais localizadas confirmam identidade
e contexto, mas ainda não sustentam uma contribuição editorial autônoma com o
mesmo nível das 27 promoções.

## Efeito no CP19

- fila canônica: **522** candidatos;
- resolvidos acumulados: **69**;
- promoções acumuladas: **60**;
- retenções acumuladas: **9**;
- fila restante: **453**, exclusivamente marcas;
- candidatos históricos: **40/40** resolvidos.

## Contratos e reprodutibilidade

O SQLite transitório continua autoridade até o corte único da v2. As alterações
são reproduzidas por `curate_brands_c06_m01a.py` e
`curate_brands_c06_m01b.py`; a migração gera JSON-LD; os pacotes de decisão e a
timeline são regenerados por scripts determinísticos. Nenhum predicado novo foi
criado e nenhuma relação foi forçada para simular completude.

Checkpoint do C06: **PASS**.
