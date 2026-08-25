"""Generate deterministic CP19 review packets for historical batches C04 and C05."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB_SCRIPTS = ROOT.parent / "atlas-web" / "scripts"
sys.path.insert(0, str(WEB_SCRIPTS))

from curate_catalog_c04 import RECORDS as C04  # noqa: E402
from curate_catalog_c05 import RECORDS as C05  # noqa: E402

TARGET = ROOT / "content" / "canonical-curation-reviews.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    entities = [load(path) for path in sorted((ROOT / "migration" / "entities").glob("*.jsonld"))]
    entity_by_name = {item["name"]: item for item in entities}
    sources = load(ROOT / "migration" / "sources.jsonld")["items"]
    source_by_url = {item.get("url"): item for item in sources}
    document = load(TARGET)
    document["reviews"] = [item for item in document.get("reviews", []) if not item["id"].startswith(("atlas:curation-review:c04-", "atlas:curation-review:c05-"))]

    for batch, records in (("C04", C04), ("C05", C05)):
        for name, (decision, title, _publisher, url, description) in records.items():
            entity = entity_by_name[name]
            source = source_by_url[url]
            review_id = entity["metadata"]["curation_review"]
            promoted = decision == "promote-editorial"
            document["reviews"].append({
                "id": review_id,
                "candidateId": entity["id"],
                "decision": decision,
                "reviewedAt": "2026-08-25",
                "rationale": (
                    "A fonte institucional individual demonstra uma consequência recuperável além da notoriedade do protótipo."
                    if promoted else
                    "A identidade permanece pesquisável, mas a fonte institucional consultada não oferece evidência individual suficiente para promoção editorial."
                ),
                "sourceIds": [source["id"]],
                "assertions": [
                    {"locator": title, "text": description},
                    {"locator": title, "text": (
                        "A decisão de promoção limita-se à consequência declarada pela fonte, sem atribuir influências adicionais."
                        if promoted else
                        "A ausência de demonstração individual impede inferir transferência tecnológica, derivação ou influência posterior."
                    )},
                ],
            })

    TARGET.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "generated": len(C04) + len(C05)}, sort_keys=True))


if __name__ == "__main__":
    main()
