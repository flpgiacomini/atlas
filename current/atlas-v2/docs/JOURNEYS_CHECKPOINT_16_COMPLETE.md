# CP16 — seis percursos editoriais completos

Data de verificação: 2026-08-24

## Resultado

O checkpoint está **concluído: 6/6 percursos completos**. Cada percurso possui
entidade e claims com evidência, capítulo narrativo, mídia local licenciada,
geografia temporal e ativo de apresentação.

| Percurso | Evidência | Narrativa | Mídia | Geografia | Estado |
| --- | --- | --- | --- | --- | --- |
| Benz Patent-Motorwagen / 1886 | sim | completa | licenciada | temporal | completo |
| Ford Model T / 1908 | sim | completa | licenciada | temporal | completo |
| Origens do Motorsport / 1955 | sim | completa | licenciada | temporal | completo |
| Volvo PV544 / 1958 | sim | completa | licenciada | temporal | completo |
| Porsche 911 / 1963 | sim | completa | licenciada | temporal | completo |
| Porsche 917 / 1969 | sim | completa | licenciada | temporal | completo |

## Fechamento editorial de 1955

- o percurso é uma lente temática e não afirma que o automobilismo nasceu em 1955;
- a tragédia é narrada sem imagem gráfica ou espetacularização;
- a divergência entre 82 e 83 vítimas permanece explícita e atribuída;
- a retirada da Mercedes-Benz durante a prova é distinguida de sua saída das
  competições ao fim da temporada, planejada anteriormente;
- as obras do circuito e a edição de 1956 aparecem como consequência documentada;
- Grand Palais e Quai de Javel conectam estreia e produção do DS;
- a imagem é declarada como ilustração editorial, não documento histórico.

## Gate automatizado

`audit_journey_coverage.py` agora falha se qualquer um dos seis percursos perder
um dos cinco componentes obrigatórios. O relatório versionado deve registrar
`completeJourneys: 6` e permanecer determinístico.

## Próximo checkpoint

O caminho crítico avança para o **CP17 — inventário cartográfico**: classificar
os 258 capítulos, definir quais possuem história espacial e fechar geometria,
fonte, precisão, confiança e validade temporal para 100% desse subconjunto.
