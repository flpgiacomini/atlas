"""Resolve every source to a sourceType, once, for every audit that needs it.

Three audits asked this question and each answered it separately, which is how
the same hole opened in all three: they took the registry's declared
`sourceType` at face value. The registry types nine manufacturer pages as
`institutional` — Mercedes-Benz Group, Porsche Newsroom, Ford, Volvo Cars and
the Mercedes-Benz Public Archive among them — and `institutional` is not a
dependent type, so the interested party was counting as its own confrontation.

The rule here is that a publisher known to be an interested party outranks the
type the source declares. The publisher is a fact about the document; the type
is an editorial label, and a generic label must never be able to launder a
manufacturer into independence. Where the publisher says nothing, the declared
type stands.

The override only ever moves a source toward dependence, never away from it, so
it cannot be used to manufacture independence either.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "migration/sources.jsonld"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dependent_publishers(classification: dict) -> dict[str, str]:
    """Publishers the policy already declares to be interested parties."""
    dependent = set(classification["dependentSourceTypes"])
    return {
        publisher: source_type
        for publisher, source_type in classification["publisherSourceTypes"].items()
        if source_type in dependent
    }


def resolve(classification: dict, documents: list[dict] | None = None) -> tuple[dict[str, str], list[str]]:
    """Map source id to sourceType, and list the sources that resolve to neither.

    `documents` supplies the entity files whose sources are declared inline; the
    migration registry is always read. An unclassified source is returned rather
    than defaulted, because the gate must not silently treat an unknown source as
    independent.
    """
    publishers = classification["publisherSourceTypes"]
    interested = dependent_publishers(classification)

    resolved: dict[str, str] = {}
    for item in load(REGISTRY)["items"]:
        publisher = item.get("publisher") or ""
        declared = item.get("sourceType")
        if override := interested.get(publisher):
            resolved[item["id"]] = override
        elif declared:
            resolved[item["id"]] = declared

    unclassified: list[str] = []
    for document in documents or []:
        for source in document.get("sources") or []:
            if not isinstance(source, dict) or source["id"] in resolved:
                continue
            publisher = source.get("publisher") or ""
            source_type = interested.get(publisher) or source.get("sourceType") or publishers.get(publisher)
            if source_type:
                resolved[source["id"]] = source_type
            else:
                unclassified.append(f'{source["id"]}: publisher {publisher or "(ausente)"}')
    return resolved, sorted(set(unclassified))
