"""Generate the complete deterministic CP19 C06/M01 review set."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / "atlas-web" / "scripts"))
from curate_brands_c06_m01a import RECORDS as M01A  # noqa: E402
from curate_brands_c06_m01b import RECORDS as M01B  # noqa: E402

TARGET = ROOT / "content" / "canonical-curation-reviews.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    entities = {load(path)["name"]: load(path) for path in sorted((ROOT / "migration" / "entities").glob("brand--*.jsonld"))}
    sources = {item.get("url"): item for item in load(ROOT / "migration" / "sources.jsonld")["items"]}
    document = load(TARGET)
    document["reviews"] = [item for item in document["reviews"] if not item["id"].startswith("atlas:curation-review:c06-")]
    records = {}
    for name, (title, _publisher, url, description) in M01A.items():
        records[name] = (title, url, "promote-editorial", description)
    for name, (title, _publisher, url, decision, _year, _milestone, description) in M01B.items():
        records[name] = (title, url, decision, description)
    for name, (title, url, decision, description) in records.items():
        entity = entities[name]
        rationale = ("A fonte institucional demonstra contribuição histórica específica suficiente para promoção editorial."
                     if decision == "promote-editorial" else
                     "A identidade e o contexto estão confirmados, mas a documentação específica ainda não justifica promoção editorial autônoma.")
        document["reviews"].append({
            "id": entity["metadata"]["curation_review"], "candidateId": entity["id"],
            "decision": decision, "reviewedAt": "2026-08-25", "rationale": rationale,
            "sourceIds": [sources[url]["id"]],
            "assertions": [
                {"locator": title, "text": description},
                {"locator": title, "text": "A decisão limita-se ao que a fonte institucional permite sustentar sem extrapolação."},
            ],
        })
    document["reviews"].sort(key=lambda item: item["id"])
    TARGET.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    promote = sum(item[2] == "promote-editorial" for item in records.values())
    print(json.dumps({"status": "PASS", "generated": len(records), "promote": promote, "retain": len(records)-promote}, sort_keys=True))


if __name__ == "__main__":
    main()
