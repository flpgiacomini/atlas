# Zotero Workspace — Atlas

## Purpose
Zotero is the source library, not the automotive database.

## Collections

ATLAS/
├── 00 Inbox
├── 01 Primary Sources
│   ├── Manufacturers
│   ├── Museums
│   ├── Archives
│   ├── Government
│   ├── Patents
│   └── Period Documents
├── 02 Secondary Sources
│   ├── Books
│   ├── Academic
│   ├── Specialist Press
│   └── Databases
├── 03 Motorsport
├── 04 Technology
├── 05 Corporate History
├── 06 Geography & Facilities
├── 07 Circuits
├── 08 Chapter I — 1885–1918
└── 99 Review

## Tags
Use few stable tags.

### Source quality/type
atlas:primary
atlas:institutional
atlas:specialist
atlas:discovery

### Workflow
atlas:inbox
atlas:reviewed
atlas:used
atlas:needs-review

### Domains
atlas:vehicle
atlas:organization
atlas:person
atlas:technology
atlas:motorsport
atlas:circuit
atlas:facility

Do not create a tag for every brand/model.

## Zotero Key
When a Source enters Atlas:
- keep its Atlas Source UUID;
- store the Zotero item key in `Source.zotero_key`.

The Zotero item key is an external identifier, not Atlas identity.

## Snapshots
Capture web snapshots when useful for:
- manufacturer archive pages;
- unstable articles;
- pages likely to change;
- evidence whose wording matters.

Do not download every page/PDF indiscriminately.
