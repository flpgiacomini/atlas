# Static export generator contract

The A8 proof was generated from the canonical SQLite snapshot using this deterministic contract:

1. Read Entity / Statement / Claim / Evidence / Source.
2. Generate one HTML file per Entity.
3. Embed that Entity's scalar facts, relationship links, evidence source blocks, related Event timeline, and two-hop graph data.
4. Generate global `search-index.json`, `graph-index.json`, `timeline.json`, and a separately curated map layer.
5. Serve as ordinary static files.

The final A9 implementation should move this contract into Astro build-time data loading rather than maintain a large custom string-template generator.
