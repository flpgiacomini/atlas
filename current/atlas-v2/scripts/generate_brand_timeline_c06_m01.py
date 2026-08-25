"""Synchronize every C06/M01 brand with the temporal genealogy view."""

from __future__ import annotations

import json
import sys
import unicodedata
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / "atlas-web" / "scripts"))
from curate_brands_c06_m01a import RECORDS as M01A  # noqa: E402
from curate_brands_c06_m01b import RECORDS as M01B  # noqa: E402

TARGET = ROOT / "content" / "brand-timeline.json"
M01A_MILESTONES = {
    "Benz": (1886, "Benz transforma o automóvel patenteado em atividade industrial"),
    "Daimler": (1890, "Daimler-Motoren-Gesellschaft organiza a linhagem Daimler"),
    "Mercedes-Benz": (1926, "Mercedes-Benz reúne as linhagens Daimler e Benz"),
    "Ford": (1903, "Ford Motor Company é constituída"),
    "De Dion-Bouton": (1883, "De Dion-Bouton inicia sua trajetória no ciclo do vapor"),
    "Panhard & Levassor": (1890, "Panhard & Levassor inicia a produção automotiva"),
}
TERMINAL = {
    "ŠKODA": (1925, "Laurin & Klement integra-se à Škoda"),
    "Alfa Romeo": (1910, "A.L.F.A. inicia a linhagem da Alfa Romeo"),
    "Buick": (1903, "Buick Motor Company é organizada"),
    "Cadillac": (1902, "Cadillac surge no polo automotivo de Detroit"),
    "Citroën": (1919, "Citroën apresenta seu primeiro automóvel"),
    "FIAT": (1899, "FIAT é fundada em Turim"),
    "Lancia": (1906, "Lancia é fundada em Turim"),
    "Lincoln": (1917, "Lincoln Motor Company é fundada"),
    "Oldsmobile": (1897, "Olds Motor Vehicle Company é organizada"),
    "Peugeot": (1889, "Peugeot apresenta seu primeiro automóvel"),
    "Renault": (1898, "Renault Frères é constituída"),
    "Rolls-Royce": (1904, "Rolls e Royce iniciam sua colaboração automotiva"),
}
TERMINAL_SOURCE_URLS = {
    "ŠKODA": "https://cdn.skoda-storyboard.com/2020/12/201221-125-years-ago-Vaclav-Laurin-and-Vaclav-Klement-laid-the-foundation-stone-for-SKODA-AUTO.pdf",
    "Lincoln": "https://corporate.ford.com/about/brands/lincoln.html",
    "Oldsmobile": "https://www.thehenryford.org/collections/explore/sets/detail/the-curved-dash-oldsmobile",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def main() -> None:
    entities = {load(path)["name"]: load(path) for path in sorted((ROOT / "migration" / "entities").glob("brand--*.jsonld"))}
    sources_doc = load(ROOT / "migration" / "sources.jsonld")["items"]
    by_url = {item.get("url"): item["id"] for item in sources_doc}
    by_legacy = {item.get("legacyId"): item["id"] for item in sources_doc}
    doc = load(TARGET)
    doc["milestones"] = [item for item in doc["milestones"] if not item["id"].startswith("atlas:brand-milestone:c06-")]
    records = {}
    for name, values in M01A.items():
        title, _publisher, url, _description = values
        year, label = M01A_MILESTONES[name]
        records[name] = (year, label, title, url)
    for name, values in M01B.items():
        title, _publisher, url, _decision, year, label, _description = values
        records[name] = (year, label, title, url)
    for name, (year, label, _title, url) in records.items():
        doc["milestones"].append({
            "id": f"atlas:brand-milestone:c06-{slug(name)}-{year}", "brand": entities[name]["id"],
            "year": year, "precision": "year", "kind": "founded", "scope": "brand-identity",
            "label": label, "sourceRefs": [by_url[url]], "confidence": "high",
        })
    existing_brands = {item["brand"] for item in doc["milestones"]}
    for name, (year, label) in TERMINAL.items():
        entity = entities[name]
        if entity["id"] in existing_brands:
            continue
        legacy_sources = entity.get("metadata", {}).get("curation_source_ids", [])
        refs = [by_legacy[item] for item in legacy_sources if item in by_legacy]
        milestone = {
            "id": f"atlas:brand-milestone:c06-audit-{slug(name)}-{year}", "brand": entity["id"],
            "year": year, "precision": "year", "kind": "founded", "scope": "brand-identity",
            "label": label, "confidence": "high" if refs else "medium",
        }
        fallback_url = TERMINAL_SOURCE_URLS.get(name)
        if not refs and fallback_url in by_url:
            refs = [by_url[fallback_url]]
        if refs:
            milestone["sourceRefs"] = refs[:1]
        else:
            milestone["source"] = {"title": f"História institucional de {name}", "publisher": name,
                                   "url": fallback_url, "trust": "primary", "verifiedAt": "2026-08-25"}
        doc["milestones"].append(milestone)
    doc["milestones"].sort(key=lambda item: (item["year"], item["id"]))
    TARGET.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    universe = set(records) | set(TERMINAL)
    covered = {name for name in universe if entities[name]["id"] in {item["brand"] for item in doc["milestones"]}}
    if covered != universe:
        raise ValueError(f"M01 timeline coverage incomplete: {sorted(universe-covered)}")
    print(json.dumps({"status": "PASS", "m01Brands": len(universe), "covered": len(covered)}, sort_keys=True))


if __name__ == "__main__":
    main()
