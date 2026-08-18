# ATLAS — Continue a partir daqui

Este é o roteiro recomendado para a próxima sessão. Não reabra A0–A8 salvo se um caso real quebrar uma decisão congelada.

## Passo 1 — Fazer o build real do A9

Trabalhe em:

```text
current/atlas-web/
```

Comandos:

```bash
npm install
npm run build
python scripts/validate_dist.py
```

Depois:
- commitar o `package-lock.json`;
- substituir `npm install` por `npm ci` em `.github/workflows/build.yml` e no fallback de GitHub Pages;
- registrar tamanho do `dist/`, quantidade real de páginas e tempo de build.

Não mude a arquitetura se ocorrer apenas um problema de CSS/UX.

## Passo 2 — Validar visualmente as rotas

Checar em desktop e viewport estreito:

- `/`
- `/e/<UUID>/`
- `/timeline/`
- `/graph/`
- `/compare/`
- `/map/`

Casos obrigatórios de navegação:
1. Porsche 917 → chassis/Entry → Attwood/Herrmann → evento.
2. Porsche 911 → gerações → evento 901→911 → duas datas disputadas → fontes.
3. Benz Patent Motor Car → Carl Benz → Benz Velo → Benz & Cie. → transição industrial de 1914.
4. Model T → tecnologia de produção.
5. Paris–Rouen → Vanderbilt → Grand Prix 1906.
6. Volvo PV544 → cinto de três pontos → Nils Bohlin.

Pergunta principal:
**parece um atlas histórico explorável ou ainda parece um navegador de banco de dados?**

## Passo 3 — Geografia release-ready

Arquivo:
`current/atlas-web/data/geography.registry.json`

Para cada Facility/Place:
- reconciliar identidade externa;
- registrar fonte da geometria;
- definir precisão;
- marcar `release_ready=true` somente após revisão;
- manter endereço e geometria como fatos separados.

Eliminar `map-points.prototype.json` do release final quando a primeira camada suficiente estiver pronta.

## Passo 4 — Fechar o workspace de pesquisa

Arquivos-base:
`current/research-workspace/`

Executar o teste real de Heurist com os cinco pilotos:
- Entity;
- temporal relationship;
- conflito 901→911;
- source/evidence;
- 917 Entry;
- 911 genealogy;
- filtro temporal;
- mapa;
- network;
- export round-trip.

Gate: 8/10 sem perda semântica crítica e sem burocracia excessiva.

Se Heurist falhar:
1. Wikibase se o problema for semântico/provenance.
2. Grist se o problema for ergonomia.
3. nodegoat somente se a condição operacional/hosting deixar de ser problema.

## Passo 5 — CI/deploy

O build deve produzir somente `dist/`.

Primário:
Cloudflare Pages.

Fallback:
GitHub Pages ou qualquer static host.

Não introduzir:
- banco em produção;
- FastAPI;
- Workers obrigatórios;
- sessão de usuário;
- API pública;
- graph DB.

## Passo 6 — A9.7 Product Complete

A9 pode ser fechado quando:
- pesquisa real entra no modelo sem gambiarra;
- SQLite valida;
- site faz build do zero;
- Pagefind busca;
- Entity Pages são agradáveis;
- provenance é visível;
- timeline/grafo/mapa/compare funcionam;
- deploy é reproduzível;
- uma sessão de curiosidade real não depende de SQL/admin;
- a infraestrutura continua menor que o problema de pesquisa.

Depois:
`v1.x = conteúdo + correções + qualidade`.

## Mudanças permitidas sem reabrir arquitetura

- CSS/layout;
- componentes Astro;
- agrupamento de conteúdo;
- filtros Pagefind;
- projeções JSON;
- enriquecimento de entidades;
- geografia reconciliada;
- novas fontes/claims/evidences;
- novos predicates realmente justificados pelo change control.

## Mudanças que exigem novo gate

- trocar SQLite como canônico;
- adicionar backend obrigatório;
- adotar graph DB como dependência;
- criar novo tipo raiz;
- transformar timeline/map/grafo em bancos paralelos;
- criar autenticação/social;
- automatizar decisão de verdade histórica por IA;
- tornar infraestrutura provider-specific.
