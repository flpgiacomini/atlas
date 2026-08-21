# Atlas v2 prototype — Design QA

- Fonte visual: `design/atlas-v2-master-target.png` (1536 × 1024)
- Evidência renderizada: `design/implementation-1969.png` (1440 × 1024 CSS px)
- Comparação: `design/comparison-source-vs-implementation.png`
- Estado validado: História, 1969, Porsche 917, modal fechado
- Navegador: Google Chrome desktop
- Resultado de build: aprovado
- Testes do worker Sites: 4/4 aprovados
- Auditoria de dependências de produção: 0 vulnerabilidades

## Evidências visuais

A captura real do Chrome foi produzida no viewport bloqueante de 1440 × 1024 e
comparada lado a lado com a referência. A implementação preserva a hierarquia
editorial, a fotografia dominante, o contraste escuro, o destaque vermelho,
o mapa contextual e a timeline persistente. As diferenças de enquadramento e
densidade da timeline são variações deliberadas do protótipo responsivo e não
comprometem o conceito aprovado.

## Verificações de interação

- Os seis percursos obrigatórios abriram o ano e o capítulo corretos:
  Benz Patent-Motorwagen (1886), Ford Model T (1908), origens do Motorsport
  (1955), Volvo PV544 (1958), Porsche 911 (1963) e Porsche 917 (1969).
- Os modos História, Mapa/Globo, Marcas, Veículos, Competições e Tecnologias
  responderam ao ano global.
- Mapa e globo alternaram o estado ativo corretamente.
- O modal imersivo abriu e fechou pelo controle visível e pela tecla Escape.
- As teclas de seta alteraram 1969 para 1968 e retornaram para 1969.
- A seleção por marcos da timeline foi exercitada pelos seis percursos.
- O console do Chrome não registrou erros.

## Achados

Nenhum defeito P0, P1 ou P2 foi encontrado nesta rodada.

## Histórico da comparação

- Primeira rodada: bloqueada pela ausência de uma conexão ativa com o Chrome.
- Segunda rodada: bloqueada por incompatibilidade entre versões do controlador.
- Rodada final: conexão restabelecida, evidências capturadas, interações
  verificadas e comparação visual aprovada.

## Polimentos não bloqueantes

- A timeline final poderá incorporar maior densidade de microeventos conforme
  os 258 capítulos forem produzidos.
- A cartografia definitiva substituirá a composição ilustrativa do protótipo
  pelas camadas temporais de MapLibre e Cesium.

final result: passed
