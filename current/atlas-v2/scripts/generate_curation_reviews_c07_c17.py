"""Generate deterministic C07-C17 review packets from the research snapshot."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT.parent / "atlas-web" / "data" / "imports" / "atlas-curation" / "brands-c07-c17.research.json"
TARGET = ROOT / "content" / "canonical-curation-reviews.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    research = {item["candidateName"]: item for item in load(SNAPSHOT)["records"]}
    entities = {load(path)["name"]: load(path) for path in sorted((ROOT / "migration" / "entities").glob("brand--*.jsonld"))}
    source_items = load(ROOT / "migration" / "sources.jsonld")["items"]
    sources = {item.get("url"): item for item in source_items}
    sources_by_legacy = {item.get("legacyId"): item for item in source_items}
    document = load(TARGET)
    prefixes = tuple(f"atlas:curation-review:c{number:02d}-" for number in range(7, 18))
    document["reviews"] = [item for item in document["reviews"] if not item["id"].startswith(prefixes)]
    selected = {name: entity for name, entity in entities.items()
                if entity.get("metadata", {}).get("curation_batch", "").split("-", 1)[0] in {f"C{number:02d}" for number in range(7, 18)}}
    for name, entity in selected.items():
        item = research[name]
        metadata = entity["metadata"]
        decision = metadata["curation_decision"]
        source = sources_by_legacy[metadata["curation_source_ids"][0]]
        if item["status"] == "matched":
            assertion = ("A página e suas categorias identificam o candidato no contexto automotivo; "
                         f"o texto consultado é rastreado pelo SHA-256 {item.get('extractSha256')} sem redistribuição integral.")
            locator = f"revision {item.get('revisionId')}"
        else:
            assertion = entity.get("description", "")
            locator = source["title"]
        document["reviews"].append({
            "id": entity["metadata"]["curation_review"], "candidateId": entity["id"],
            "decision": decision, "reviewedAt": metadata["curation_reviewed_at"],
            "rationale": ("A triagem de relevância é confirmada por uma correspondência automotiva individual; a promoção não autoriza extrapolar além da fonte."
                          if decision == "promote-editorial" else
                          "A pesquisa não obteve correspondência individual inequívoca. O registro é preservado no catálogo sem publicar novas alegações históricas."),
            "sourceIds": [source["id"]],
            "assertions": [
                {"locator": locator, "text": assertion},
                {"locator": source["title"], "text": "Relações genealógicas e contribuições específicas exigem evidência própria."},
            ],
        })
    document["reviews"].sort(key=lambda entry: entry["id"])
    TARGET.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "generated": len(selected)}, sort_keys=True))


if __name__ == "__main__":
    main()
