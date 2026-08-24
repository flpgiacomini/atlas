"""Build the deterministic editorial cartography inventory for 1769-2026."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "content" / "spatial-inventory.json"

BROAD_CONTEXTS = {
    "Europa", "França", "Alemanha", "Reino Unido", "Estados Unidos",
    "Japão", "Mundo", "Mundo industrializado", "Indústria global",
    "União Europeia", "Coreia do Sul",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parsed_year(value: object) -> int | None:
    match = re.match(r"^(\d{4})", str(value or ""))
    return int(match.group(1)) if match else None


def mapped_intervals() -> dict[str, list[tuple[int, int]]]:
    result: dict[str, list[tuple[int, int]]] = {}
    for path in sorted((ROOT / "content" / "geography").glob("*.geojson")):
        for feature in load(path).get("features", []):
            entity = feature.get("properties", {}).get("entity")
            validity = feature.get("properties", {}).get("validity", {})
            start = parsed_year(validity.get("from"))
            end = parsed_year(validity.get("until"))
            if entity and start is not None and end is not None:
                result.setdefault(entity, []).append((start, end))
    return result


def classify(chapter: dict, journey_years: set[int]) -> tuple[str, str]:
    place = chapter["place"]
    asset = chapter["asset"]
    if chapter["year"] in journey_years:
        return "interactive-required", "percurso editorial obrigatório sincronizado ao ano global"
    if asset.endswith("geography.webp"):
        return "interactive-required", "capítulo explicitamente estruturado pela geografia"
    if asset.endswith("motorsport.webp"):
        return "interactive-required", "competição depende de circuito, etapa ou deslocamento"
    if " · " in place:
        return "interactive-required", "múltiplos lugares formam uma relação ou deslocamento histórico"
    if place in BROAD_CONTEXTS or any(token in place.lower() for token in ("global", "mercados", "mundo")):
        return "static-sufficient", "escala regional ou global pede contexto editorial, não navegação de precisão"
    return "static-sufficient", "um lugar contextual pode ser representado por mapa editorial ou cartão ancorado"


def build() -> dict:
    chapters = load(ROOT / "content" / "annual-chapters.json")["chapters"]
    journeys = load(ROOT / "content" / "journeys.json")["journeys"]
    journey_entities = {item["year"]: item["entity"] for item in journeys}
    journey_years = set(journey_entities)
    mapped = mapped_intervals()
    items = []
    for chapter in chapters:
        mode, rationale = classify(chapter, journey_years)
        geometry_entity = journey_entities.get(chapter["year"], chapter["entity"])
        covered = any(start <= chapter["year"] <= end for start, end in mapped.get(geometry_entity, []))
        items.append({
            "year": chapter["year"],
            "entity": chapter["entity"],
            "geometryEntity": geometry_entity,
            "place": chapter["place"],
            "mode": mode,
            "rationale": rationale,
            "geometryStatus": "covered" if covered else ("pending" if mode == "interactive-required" else "not-required"),
        })
    summary = {
        "chapters": len(items),
        "interactiveRequired": sum(item["mode"] == "interactive-required" for item in items),
        "staticSufficient": sum(item["mode"] == "static-sufficient" for item in items),
        "notSpatial": sum(item["mode"] == "not-spatial" for item in items),
        "interactiveCovered": sum(item["mode"] == "interactive-required" and item["geometryStatus"] == "covered" for item in items),
        "interactivePending": sum(item["mode"] == "interactive-required" and item["geometryStatus"] == "pending" for item in items),
    }
    return {
        "version": "1.0.0",
        "policy": {
            "interactive-required": "A relação espacial é necessária para compreender o capítulo e exige GeoJSON temporal validado.",
            "static-sufficient": "A geografia contextual pode usar mapa editorial estático ou cartão; GeoJSON interativo não bloqueia o capítulo.",
            "not-spatial": "A dimensão espacial não acrescenta compreensão material e é conscientemente dispensada.",
        },
        "summary": summary,
        "items": items,
    }


def main() -> None:
    OUTPUT.write_text(json.dumps(build(), ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(build()["summary"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
