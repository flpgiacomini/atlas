"""Build deterministic, lazy-loadable Atlas v2 publication bundles."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "migration"
DEFAULT_OUTPUT = ROOT / "bundles"
PERIODS = (
    ("1769-1885", 1769, 1885), ("1886-1918", 1886, 1918),
    ("1919-1939", 1919, 1939), ("1940-1959", 1940, 1959),
    ("1960-1979", 1960, 1979), ("1980-1999", 1980, 1999),
    ("2000-2009", 2000, 2009), ("2010-2019", 2010, 2019),
    ("2020-2026", 2020, 2026),
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")


def slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.lower()).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "global"


def claim_years(entity: dict) -> list[int]:
    values: list[int] = []
    for claim in entity.get("claims", []):
        obj = claim.get("object")
        candidates = [claim.get("validity", {}).get("from"), claim.get("validity", {}).get("until")]
        if isinstance(obj, int):
            candidates.append(obj)
        elif isinstance(obj, dict) and obj.get("type") == "date":
            candidates.append(obj.get("value"))
        for candidate in candidates:
            match = re.match(r"^(\d{4})", str(candidate or ""))
            if match and 1769 <= int(match.group(1)) <= 2026:
                values.append(int(match.group(1)))
    metadata_year = entity.get("metadata", {}).get("candidate_year")
    if isinstance(metadata_year, int) and 1769 <= metadata_year <= 2026:
        values.append(metadata_year)
    return sorted(set(values))


def summary(entity: dict) -> dict:
    years = claim_years(entity)
    sources = sorted({source for claim in entity.get("claims", []) for source in claim.get("sources", [])})
    metadata = entity.get("metadata", {})
    return {
        "id": entity["id"], "type": entity["type"], "name": entity["name"],
        "aliases": entity.get("aliases", []), "description": entity.get("description"),
        "yearStart": years[0] if years else None, "yearEnd": years[-1] if years else None,
        "years": years, "claimCount": len(entity.get("claims", [])), "sourceCount": len(sources),
        "editorialLevel": metadata.get("editorial_level", "unknown"),
        "region": metadata.get("region_cluster", "Global / não classificado"),
    }


def period_for(year: int | None) -> str:
    if year is not None:
        for name, start, end in PERIODS:
            if start <= year <= end:
                return name
    return "undated"


def build(output: Path) -> dict:
    temp = output.with_name(output.name + ".tmp")
    if temp.exists():
        shutil.rmtree(temp)
    temp.mkdir(parents=True)
    migrated = [load(path) for path in sorted((MIGRATION / "entities").glob("*.jsonld"))]
    by_id = {entity["id"]: entity for entity in migrated}
    for path in sorted((ROOT / "content/entities").glob("*.jsonld")):
        entity = load(path)
        by_id.setdefault(entity["id"], entity)
    entities = list(by_id.values())
    summaries = sorted((summary(entity) for entity in entities), key=lambda item: item["id"])
    source_by_id = {source["id"]: source for source in load(MIGRATION / "sources.jsonld")["items"]}
    for entity in entities:
        for source in entity.get("sources", []):
            source_by_id.setdefault(source["id"], source)

    categories: dict[str, list[dict]] = defaultdict(list)
    periods: dict[str, list[dict]] = defaultdict(list)
    regions: dict[str, list[dict]] = defaultdict(list)
    for name, _, _ in PERIODS:
        periods[name] = []
    for item in summaries:
        categories[slug(item["type"])].append(item)
        periods[period_for(item["yearStart"])].append(item)
        regions[slug(item["region"])].append(item)

    files: list[dict] = []
    family_kind = {"categories": "category", "periods": "period", "regions": "region"}
    for family, groups in (("categories", categories), ("periods", periods), ("regions", regions)):
        for key, items in sorted(groups.items()):
            relative = f"{family}/{key}.json"
            payload = {"version": "2.0.0", "kind": family_kind[family], "key": key, "count": len(items), "items": items}
            dump(temp / relative, payload)
            files.append({"path": relative, "kind": family_kind[family], "key": key, "count": len(items)})

    journey_config = load(ROOT / "content/journeys.json")["journeys"]
    media_by_entity: dict[str, list[dict]] = defaultdict(list)
    media_items = load(ROOT / "content" / "media-manifest.json")["items"]
    media_by_id = {item["id"]: item for item in media_items}
    for media in media_items:
        media_by_entity[media["journeyEntity"]].append(media)
    journey_items = []
    for journey in journey_config:
        entity = by_id.get(journey.get("entity"))
        source_ids = sorted({source for claim in (entity or {}).get("claims", []) for source in claim.get("sources", [])})
        journey_items.append({
            **journey,
            "record": summary(entity) if entity else None,
            "claims": (entity or {}).get("claims", []),
            "sources": [source_by_id[source] for source in source_ids],
            "media": sorted(media_by_entity.get(journey["entity"], []), key=lambda item: item["id"]),
            "coverageState": "connected" if entity else "editorial-gap",
        })
    dump(temp / "journeys.json", {"version": "2.0.0", "count": len(journey_items), "items": journey_items})
    files.append({"path": "journeys.json", "kind": "journeys", "key": "required-six", "count": len(journey_items)})

    annual_config = load(ROOT / "content/annual-chapters.json")
    media_decisions = {
        item["year"]: item
        for item in load(ROOT / "content/story-media-decisions.json")["decisions"]
    }
    annual_items = []
    for chapter in annual_config["chapters"]:
        entity = by_id.get(chapter["entity"])
        source_ids = sorted({source for claim in entity.get("claims", []) for source in claim.get("sources", [])})
        media_decision = media_decisions[chapter["year"]]
        resolved_media = [media_by_id[item] for item in media_decision["mediaIds"]]
        annual_items.append({
            **chapter,
            "asset": resolved_media[0]["file"] if resolved_media else chapter["asset"],
            "record": summary(entity),
            "claims": entity.get("claims", []),
            "sources": [source_by_id[source] for source in source_ids],
            "mediaDecision": media_decision,
            "media": resolved_media,
            "coverageState": "authored",
        })
    annual_items.sort(key=lambda item: item["year"])
    dump(temp / "annual-chapters.json", {"version": annual_config["version"], "count": len(annual_items), "items": annual_items})
    files.append({"path": "annual-chapters.json", "kind": "annual-chapters", "key": "exact-year", "count": len(annual_items)})

    brand_timeline = load(ROOT / "content/brand-timeline.json")
    milestones = sorted(brand_timeline["milestones"], key=lambda item: (item["year"], item["id"]))
    dump(temp / "brand-timeline.json", {"version": brand_timeline["version"], "count": len(milestones), "items": milestones})
    files.append({"path": "brand-timeline.json", "kind": "brand-timeline", "key": "lifecycle-milestones", "count": len(milestones)})

    brand_relations = load(ROOT / "content/brand-relations.json")
    relations = sorted(brand_relations["relations"], key=lambda item: (item["validFrom"], item["id"]))
    dump(temp / "brand-relations.json", {"version": brand_relations["version"], "count": len(relations), "items": relations})
    files.append({"path": "brand-relations.json", "kind": "brand-relations", "key": "corporate-relations", "count": len(relations)})

    geography_features = []
    for path in sorted((ROOT / "content/geography").glob("*.geojson")):
        collection = load(path)
        for feature in collection.get("features", []):
            geography_features.append({**feature, "properties": {**feature.get("properties", {}), "dataset": path.name}})
    geography_features.sort(key=lambda item: str(item.get("id", "")))
    geography = {"type": "FeatureCollection", "version": "2.0.0", "count": len(geography_features), "features": geography_features}
    dump(temp / "geography.json", geography)
    files.append({"path": "geography.json", "kind": "geography", "key": "temporal-features", "count": len(geography_features)})

    dump(temp / "index.json", {"version": "2.0.0", "count": len(summaries), "items": summaries})
    files.append({"path": "index.json", "kind": "index", "key": "entities", "count": len(summaries)})
    for item in files:
        item["sha256"] = hashlib.sha256((temp / item["path"]).read_bytes()).hexdigest()
    manifest = {
        "version": "2.0.0", "entityCount": len(summaries), "files": files,
        "periods": [{"id": name, "from": start, "until": end} for name, start, end in PERIODS],
        "sourceMigrationSha256": hashlib.sha256((MIGRATION / "checksums.json").read_bytes()).hexdigest(),
    }
    dump(temp / "manifest.json", manifest)
    if output.exists():
        shutil.rmtree(output)
    temp.replace(output)
    return {"status": "PASS", "entities": len(summaries), "bundles": len(files), "journeys": len(journey_items)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(build(args.output.resolve()), sort_keys=True))


if __name__ == "__main__":
    main()
