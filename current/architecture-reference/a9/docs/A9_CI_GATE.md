# A9 CI / Build Gate

The ChatGPT execution environment has Node 22/npm 10 but does not have Astro/Pagefind packages cached,
and network installation is unavailable.

Therefore the durable validation moves to repository CI.

## `build.yml`
For every PR/push:
1. Python 3.13
2. Node 22
3. `npm install`
4. canonical export
5. Astro static build
6. Pagefind indexing
7. `validate_dist.py`
8. upload `dist/` as artifact

## `validate_dist.py`
Fails when:
- an Entity route is missing;
- timeline/graph/map/compare route is missing;
- Pagefind did not generate its bundle;
- graph/compare publication JSON is missing.

## Deployment
Cloudflare Pages can use the same `npm run build` + `dist/` contract.
A manual GitHub Pages workflow is included only as provider-independent fallback.

## Lockfile
A package lock is intentionally not fabricated in this environment.
The first real `npm install` should commit the generated `package-lock.json`;
after that CI should be changed from `npm install` to `npm ci`.
