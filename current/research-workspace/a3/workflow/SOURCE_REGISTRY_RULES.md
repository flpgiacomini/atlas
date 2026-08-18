# Source Registry Rules v1.0

## Source is not Evidence
Source = document/page/book/archive/database record.
Evidence = precise location inside that Source used for a Claim.

## Source tiers
A — primary/direct historical or corporate/legal/technical record
B — institutional archive/museum/government/organizer
C — specialist historiography/journalism
D — structured database/encyclopedic source
E — community/discovery lead

Tier does not set Statement confidence automatically.

## Duplicate Source rule
Same URL/title imported twice:
- reconcile first;
- preserve one canonical Source UUID;
- Claims may point to different Evidence locators in the same Source.

## Accessed date
Record accessed_at for web sources when they become Evidence.

## Evidence locator
Prefer, in order:
- page
- section/heading
- table/figure
- paragraph/fragment
- archive/catalogue identifier

Do not use only "homepage" when a more precise locator is available.

## Excerpts
Store only short excerpts when necessary for research context and legally appropriate.
The source URL/citation remains primary.
