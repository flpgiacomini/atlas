# Checkpoint — capítulos precursores 01

Data: 2026-08-24

## Resultado

- 11 capítulos-âncora autorais entre 1769 e 1885.
- 11/11 capítulos ligados a entidade, claims, evidências e fontes recuperáveis.
- Novo bundle `annual-chapters.json`, carregado sob demanda pela SPA.
- Novo validador canônico integrado ao CI.
- Anos sem capítulo deixam de herdar silenciosamente a história mais próxima.
- Lacunas passam a ser exibidas como `editorial-gap`, com o ano contextual de
  referência explicitado.

## Anos cobertos

1769, 1801, 1803, 1807, 1862, 1863, 1873, 1875, 1878, 1884 e 1885.

O arco cobre o fardier de Cugnot, o vapor de alta pressão, a experiência urbana
de Trevithick, a combustão de Rivaz, as formulações de dois e quatro tempos,
Lenoir, L’Obéissante e a convergência imediatamente anterior a 1886.

## QA

- Build: 260 páginas.
- Testes: 5/5.
- Bundle: 43 projeções, SHA-256 determinístico.
- Navegador real: 1769 e 1885 exibem capítulos exatos; 1770 exibe lacuna
  editorial explícita; nenhum erro de console ao final do percurso.

## Próximo gate

Transformar os intervalos entre âncoras em capítulos de continuidade escritos e
referenciados. O período só será considerado completo quando 117/117 anos de
1769 a 1885 tiverem capítulo editorial proporcional à evidência, sem replicação
automática de texto.
