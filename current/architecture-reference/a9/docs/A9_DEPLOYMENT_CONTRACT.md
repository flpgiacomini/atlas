# A9 Deployment Contract

## Production artifact
`dist/` only.

## Primary
Cloudflare Pages:
- framework preset: Astro or custom static build;
- build command: `npm run build`;
- output directory: `dist`;
- no Pages Functions;
- no D1/KV/R2 dependency;
- `_headers` is copied from `public/`.

## Fallback
Any host capable of serving static files.

The site architecture must not depend on:
- Cloudflare Workers;
- server-side sessions;
- database credentials;
- provider-specific routing logic.

## Local smoke
After build:
`python -m http.server -d dist 8000`

## Search
Pagefind runs after Astro and writes into `dist/pagefind/`.

## Geography
No runtime geocoding.
No public Nominatim API call from the browser.
