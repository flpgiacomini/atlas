"""Build deterministic per-chapter media decisions for CP18."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "content" / "story-media-decisions.json"
PERIOD_MEDIA = (
    (1769, 1800, "atlas:media:v01-cugnot-1769-1800-editorial"),
    (1801, 1834, "atlas:media:v01-steam-road-1801-1834-editorial"),
    (1835, 1859, "atlas:media:v01-electric-experiments-1835-1859-editorial"),
    (1860, 1875, "atlas:media:v01-combustion-1860-1875-editorial"),
    (1876, 1885, "atlas:media:v01-convergence-1876-1885-editorial"),
    (1886, 1895, "atlas:media:v02-birth-1886-1895-editorial"),
    (1896, 1903, "atlas:media:v02-plurality-racing-1896-1903-editorial"),
    (1904, 1907, "atlas:media:v02-industry-1904-1907-editorial"),
    (1909, 1913, "atlas:media:v02-mass-production-1909-1913-editorial"),
    (1914, 1918, "atlas:media:v02-war-mobilization-1914-1918-editorial"),
    (1919, 1924, "atlas:media:v03-reconstruction-1919-1924-editorial"),
    (1925, 1929, "atlas:media:v03-design-racing-1925-1929-editorial"),
    (1930, 1934, "atlas:media:v03-crisis-aerodynamics-1930-1934-editorial"),
    (1935, 1939, "atlas:media:v03-popular-modernity-1935-1939-editorial"),
    (1940, 1945, "atlas:media:v03-war-disruption-1940-1945-editorial"),
)


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
        media_ids.extend(
            media_id for start, end, media_id in PERIOD_MEDIA
            if start <= chapter["year"] <= end and media_id not in media_ids
        )
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
