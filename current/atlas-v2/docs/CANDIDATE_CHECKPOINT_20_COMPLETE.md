# CP20 — QA do candidato v2 completo

Data de fechamento local: 2026-08-25.

## Resultado

O candidato v2 encerra o CP20 com **PASS**. O contrato canônico, as 258 rotas
anuais, os seis percursos obrigatórios, a busca temporal, o modal de entidade e
as projeções especializadas foram exercitados no build destinado a `/atlas/`.

## Gates executados

1. **Semântica e conteúdo: PASS.** 522/522 decisões C18, 920 entidades
   migradas, 966 entidades publicáveis nos bundles, 258/258 capítulos, 258/258
   decisões de mídia e 95/95 histórias espacialmente interativas cobertas.
2. **Determinismo: PASS.** Migração e bundles produziram hashes idênticos em
   duas execuções consecutivas; 53 bundles foram validados.
3. **Aplicação: PASS.** `astro check` sem diagnósticos, cinco testes unitários,
   260 páginas estáticas, 404 e assets obrigatórios.
4. **Cartografia: PASS.** MapLibre e Cesium são dependências locais; 97
   geometrias temporais compõem o bundle único. O mapa fornece projeção local e
   alternativa vetorial/textual; o globo carrega o runtime e os workers Cesium
   apenas quando solicitado.
5. **Chrome desktop: PASS.** História, timeline, Mapa, Globo, busca e modal da
   Porsche 917 foram verificados em navegador real, sem erros ou avisos no
   console e sem alteração de URL ao abrir a entidade.
6. **Mobile smoke: PASS.** Em 390 x 844, navegação de modos, mapa e timeline
   continuam acessíveis, com painel especializado simplificado e rolagem
   horizontal deliberada nos controles temporais.
7. **Orçamento de entrega: PASS.** JavaScript inicial: 213.129 bytes em dois
   módulos. MapLibre permanece em chunk sob demanda; Cesium, com 5.974.765
   bytes no runtime principal, não aparece no HTML inicial. O artefato total tem
   aproximadamente 140 MB por conter o runtime/Workers local do Cesium.

## Decisões de lançamento

- O site v1 permanece público até o corte único do CP21.
- O tamanho local do Cesium é uma limitação conhecida, mitigada por lazy load;
  otimização adicional não bloqueia o corte.
- A alternativa textual é parte do contrato, inclusive quando WebGL estiver
  indisponível.
- O CP21 deve trocar o artefato do Pages, executar smoke público, registrar URL
  e commit, criar tag e release. Nenhuma alteração editorial é necessária para
  iniciar esse corte.

Checkpoint CP20: **PASS**. Próximo e único checkpoint: **CP21 — corte v2**.
