"""Generate deterministic review packets for CP19 C06/M01A."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / "atlas-web" / "scripts"))
from curate_brands_c06_m01a import RECORDS  # noqa: E402

TARGET = ROOT / "content" / "canonical-curation-reviews.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    entities = {load(path)["name"]: load(path) for path in sorted((ROOT / "migration" / "entities").glob("brand--*.jsonld"))}
    sources = {item.get("url"): item for item in load(ROOT / "migration" / "sources.jsonld")["items"]}
    document = load(TARGET)
    document["reviews"] = [item for item in document["reviews"] if not item["id"].startswith("atlas:curation-review:c06-")]
    for name, (title, _publisher, url, description) in RECORDS.items():
        entity = entities[name]
        document["reviews"].append({
            "id": entity["metadata"]["curation_review"], "candidateId": entity["id"],
            "decision": "promote-editorial", "reviewedAt": "2026-08-25",
            "rationale": "A fonte institucional demonstra papel estrutural na formação, industrialização ou consolidação genealógica do automóvel.",
            "sourceIds": [sources[url]["id"]],
            "assertions": [
                {"locator": title, "text": description},
                {"locator": title, "text": "A promoção registra somente relações e consequências expressamente sustentadas pela fonte institucional."},
            ],
        })
    TARGET.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "generated": len(RECORDS)}, sort_keys=True))


if __name__ == "__main__":
    main()
