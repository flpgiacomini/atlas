# Checkpoint — registry temporal de marcas

Data: 2026-08-21

## Resultado

Foi criado o primeiro registry canônico de marcos de ciclo de vida de marcas.
Ele não altera silenciosamente as entidades migradas e não confunde marca,
companhia operadora ou proprietário.

- 9 marcos validados;
- 7 marcas conectadas;
- fontes institucionais primárias ou fontes já migradas;
- precisão anual, mensal ou diária explícita;
- bundle determinístico `brand-timeline.json`;
- projeção carregada sob demanda pelo rio de marcas.

## Marcas do primeiro núcleo

Renault, FIAT, Ford, Lancia, Citroën, Mercedes-Benz e Bugatti.

Os marcos de Renault, Ford e Lancia apresentados neste lote descrevem a
organização operadora. Eles não são publicados como data automática de criação
da identidade comercial. FIAT, Citroën, Mercedes-Benz e os renascimentos da
Bugatti possuem escopo explícito de identidade da marca.

## Gate

`validate_brand_timeline.py` bloqueia:

- marca, evento ou fonte canônica inexistente;
- marco sem fonte;
- URL externa não HTTPS;
- fonte externa que não seja primária neste lote inicial;
- ano ou precisão inválidos;
- precisão diária ou mensal sem data correspondente;
- mistura de escopo fora do vocabulário controlado.

## Próxima expansão

Adicionar as marcas de maior centralidade histórica em lotes pequenos,
priorizando predecessoras, sucessoras, renomes, fusões, aquisições e extinções.
O rio só desenhará uma conexão genealógica quando os dois nós, o tipo da relação,
o intervalo e a fonte estiverem validados.
