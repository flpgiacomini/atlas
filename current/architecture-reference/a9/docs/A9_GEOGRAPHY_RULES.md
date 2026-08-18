# ATLAS Geography Publication Rules v1

## Separation of concerns

`Facility/Place identity` and `map geometry` are different layers.

Canonical/research facts:
- Facility or Place identity;
- located_in relationships;
- verified official address/location text;
- external identifiers when reconciled.

Publication geometry:
- point/polygon used by map rendering;
- precision;
- source;
- reconciliation status;
- release readiness.

## Hard rule
An approximate point must never be relabeled as canonical merely because it looks correct on a map.

## Release statuses
- `verified`: geometry externally reconciled and source recorded.
- `provisional`: useful during development, excluded from v1 release map.
- `historical_approximation`: deliberately approximate historical location, clearly labeled.
- `unknown`: no geometry.

## Geocoding
Do not geocode at page-load/runtime.

For a one-time research batch, Nominatim may be used only if its public usage policy is followed:
- maximum 1 request/second;
- identifying User-Agent/Referer;
- results cached;
- no autocomplete;
- no recurring bulk job.

The publication build consumes cached/reconciled results only.

## Basemap
Leaflet is renderer, not data authority.
OSM public raster tiles are development/default-view infrastructure only and must respect OSMF attribution/cache policies.

## A9.2 status
Official address truth is now separated from geometry.
Existing prototype coordinates remain `provisional` and are **not release-ready**.
A9.2 closes only after the release map contains reconciled geometry instead of prototype approximations.
