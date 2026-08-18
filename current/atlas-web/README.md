# ATLAS Web — A9 Foundation

Static production frontend for Atlas v1.

## Versions
- Astro 7.2.2
- Pagefind 1.5.2

## Local setup
```bash
npm install
npm run dev
```

## Production build
```bash
npm run build
```

The build always starts by regenerating publication data from `data/atlas.sqlite`.

## Build contract
`data/atlas.sqlite`
→ `scripts/export_web.py`
→ Astro static routes
→ `astro build`
→ `pagefind --site dist`
→ deploy `dist/` to any static host.

## No production backend
No FastAPI, database server, API credentials or server-side rendering is required.

## Current generated-data validation
- pages exported: 334
- graph edges: 326
- timeline events: 102

## Current limitation in this artifact
Node packages are declared but not installed here, so the Astro build itself was not executed in the ChatGPT environment.
The Python canonical export was executed successfully.
