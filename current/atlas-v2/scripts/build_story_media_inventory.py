"""Build deterministic per-chapter media decisions for CP18."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "content" / "story-media-decisions.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    chapters = load(ROOT / "content" / "annual-chapters.json")["chapters"]
    journeys = {item["year"]: item["entity"] for item in load(ROOT / "content" / "journeys.json")["journeys"]}
    media = load(ROOT / "content" / "media-manifest.json")["items"]
    media_by_entity: dict[str, list[str]] = {}
    for item in media:
        media_by_entity.setdefault(item["journeyEntity"], []).append(item["id"])

    decisions = []
    for chapter in sorted(chapters, key=lambda item: item["year"]):
        candidates = {chapter["entity"], journeys.get(chapter["year"])}
        media_ids = sorted({media_id for entity in candidates if entity for media_id in media_by_entity.get(entity, [])})
        has_media = bool(media_ids)
        decisions.append({
            "year": chapter["year"],
            "entity": chapter["entity"],
            "mode": "licensed-media" if has_media else "text-led",
            "mediaIds": media_ids,
            "rationale": (
                "Mídia editorial específica, local e licenciada disponível para esta história."
                if has_media else
                "Composição textual temporária; mídia específica ainda exige seleção, licença e revisão editorial."
            ),
            "reviewedAt": "2026-08-24",
        })

    OUTPUT.write_text(
        json.dumps({"version": "2.0.0", "decisions": decisions}, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "PASS", "decisions": len(decisions), "licensedMedia": sum(bool(item["mediaIds"]) for item in decisions), "textLed": sum(item["mode"] == "text-led" for item in decisions)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
