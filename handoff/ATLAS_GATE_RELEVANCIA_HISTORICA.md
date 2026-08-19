# Atlas — gate de relevância histórica

Baseline: 19 de agosto de 2026  
Aplicação: marcas, conceitos, protótipos e automóveis únicos  
Resultado possível: `include`, `context_only`, `hold` ou `exclude`

## Princípio

Dimensão de catálogo não equivale a importância histórica. O AllCarIndex funciona como
instrumento de descoberta, mas o Atlas publica somente entidades que ajudam a explicar uma
mudança verificável na história do automóvel. Raridade, preço, potência, aparência exótica,
notoriedade recente ou existência de uma página externa não bastam isoladamente.

## Eixos de contribuição

Cada candidato recebe de zero a dois pontos em cada eixo:

| Código | Eixo | 0 | 1 | 2 |
|---|---|---|---|---|
| TEC | Tecnologia | nenhuma contribuição demonstrada | experimento relevante | introduziu, validou ou transferiu solução influente |
| IND | Indústria e produção | sem efeito | caso regional ou de pequena escala documentado | alterou processo, escala, cadeia ou estrutura industrial |
| DES | Design e arquitetura | exercício isolado | linguagem reconhecível ou ponte entre projetos | criou paradigma, tipologia ou influência comprovada |
| SEG | Segurança, ambiente e regulação | ausente | pesquisa ou resposta normativa | modificou prática, norma ou adoção ampla |
| ESP | Competição e desempenho | sem resultado histórico | participação ou laboratório relevante | marco esportivo ou transferência tecnológica comprovada |
| SOC | Impacto social e cultural | curiosidade | representação significativa | transformou acesso, comportamento, cultura ou imaginário |
| GEO | Relevância regional | duplicação de narrativa conhecida | documenta trajetória local | inaugura ou reorganiza indústria/mobilidade regional |
| GEN | Genealogia | isolado | explica um modelo ou marca | elo indispensável entre múltiplas entidades centrais |

## Decisão

- **include:** mínimo de 5 pontos, pelo menos dois eixos, uma fonte primária/institucional e
  uma fonte historiográfica independente. Um único eixo com nota 2 pode justificar inclusão
  excepcional quando o efeito histórico estiver documentado.
- **context_only:** 3–4 pontos ou contribuição importante apenas para explicar entidade A.
- **hold:** indício de relevância, mas fontes, identidade, datação ou influência insuficientes.
- **exclude:** 0–2 pontos, réplica, restomod sem efeito histórico demonstrado, proposta sem
  artefato verificável, identidade comercial sem automóvel ou item cuja única distinção seja
  raridade/luxo.

Nenhuma pontuação é gerada automaticamente a partir de popularidade, número de resultados,
preço de leilão ou descrição promocional.

## Regras por categoria

### Marcas

Uma marca entra quando contribuiu em produto, indústria, competição, tecnologia, design,
mobilidade regional ou genealogia. Marcas efêmeras podem entrar; marcas com muitos modelos
podem ficar de fora se não houver contribuição demonstrável. Fabricante, grupo e marca não
são fundidos para inflar relevância.

### Conceitos e protótipos

Um conceito somente entra se houver pelo menos uma destas evidências:

- recurso transferido a automóvel de produção;
- programa experimental com resultado técnico documentado;
- criação ou consolidação de linguagem de design influente;
- origem demonstrável de novo segmento, arquitetura ou estratégia de marca;
- papel relevante em segurança, energia, aerodinâmica, materiais ou automação;
- impacto público documentado que alterou a prática de apresentação do automóvel.

Preview quase idêntico ao modelo lançado será qualifier/evento do veículo de produção, não
uma Entity Page autônoma, salvo quando teve trajetória histórica própria.

### One-offs

Encomenda individual não é relevante por definição. Um one-off entra apenas quando funciona
como laboratório técnico, recordista, obra de design influente, elo de coachbuilding, caso
industrial singular ou artefato cultural com efeito histórico demonstrado. Personalizações
recentes de luxo permanecem fora até existir distância histórica e evidência de influência.

## Evidência obrigatória

O AllCarIndex pode originar um candidato, nunca ser a única fonte de um statement. A promoção
exige documento do fabricante, patente, arquivo, museu, publicação contemporânea ou acervo
institucional, acrescido de análise independente quando a alegação envolver prioridade ou
influência. Datas, produção e termos como “primeiro” recebem qualifier de precisão.

## Auditoria

O arquivo `current/atlas-web/data/historical-significance.candidates.csv` registra a primeira
seleção de conceitos e one-offs. `decision=include_candidate` significa que a relevância
merece pesquisa aprofundada; não significa que o fato já está aprovado para o SQLite.

