#!/usr/bin/env python3
"""Apply source-backed C07-C17 decisions from the reviewed research snapshot."""

from __future__ import annotations

import json
import re
import sqlite3
import unicodedata
from pathlib import Path

from enrich_people_batch_01 import stable_uuid7

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
SNAPSHOT = ROOT / "data" / "imports" / "atlas-curation" / "brands-c07-c17.research.json"
NOW = "2026-08-25T23:55:00+00:00"


def slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def main() -> None:
    research = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    records = [item for item in research["records"] if item["status"] == "matched"]
    db = sqlite3.connect(DB)
    applied = []
    try:
        for item in records:
            name = item["candidateName"]
            row = db.execute("SELECT id, metadata_json FROM entity WHERE canonical_name=? AND entity_type='brand'", (name,)).fetchone()
            if not row:
                raise ValueError(f"brand candidate not found: {name}")
            metadata = json.loads(row[1] or "{}")
            wave = metadata.get("wave")
            if wave not in {f"M{number:02d}" for number in range(2, 13)}:
                raise ValueError(f"candidate outside C07-C17: {name} / {wave}")
            batch = f"C{int(wave[1:]) + 5:02d}-{wave}"
            url = item["url"]
            source_id = stable_uuid7("source:" + url)
            notes = json.dumps({
                "curationBatch": batch, "matchMethod": item["matchMethod"],
                "wikidataId": item.get("wikidataId"), "pageId": item.get("pageId"),
                "revisionId": item.get("revisionId"), "revisionTimestamp": item.get("revisionTimestamp"),
            }, ensure_ascii=False, sort_keys=True)
            db.execute("""INSERT INTO source(id,source_type,title,publisher,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at)
                VALUES(?,'reference',?,'Wikipedia contributors',?,'2026-08-25','en','B',?,?,?,?)
                ON CONFLICT(id) DO UPDATE SET title=excluded.title,accessed_at=excluded.accessed_at,
                    external_ids_json=excluded.external_ids_json,notes=excluded.notes,updated_at=excluded.updated_at""",
                (source_id, item["title"], url, json.dumps({"wikidata": item.get("wikidataId")}, sort_keys=True), notes, NOW, NOW))
            region = metadata.get("region_cluster", "seu contexto regional")
            description = (
                f"Marca ou fabricante automotivo do recorte {region}. A revisão {batch} confirmou sua identidade "
                f"em fonte individual e preservou sua incorporação editorial ao Atlas; afirmações históricas "
                f"mais específicas permanecem limitadas ao resumo e às referências da fonte registrada."
            )
            metadata.update({
                "curation_batch": batch, "curation_review": f"atlas:curation-review:{batch.lower()}-{slug(name)}",
                "curation_reviewed_at": "2026-08-25", "curation_decision": "promote-editorial",
                "curation_source_ids": [source_id], "editorial_level": "catalog",
                "promotion_state": "approved_pending_v2_cut", "verification_state": "source_backed",
                "verified_at": "2026-08-25", "research_match_method": item["matchMethod"],
                "research_wikidata_id": item.get("wikidataId"), "research_extract_sha256": item.get("extractSha256"),
            })
            metadata.pop("research_extract", None)
            db.execute("UPDATE entity SET description=?,metadata_json=?,updated_at=? WHERE id=?",
                       (description, json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, row[0]))
            applied.append({"name": name, "batch": batch})
        db.commit()
    except Exception:
        db.rollback(); raise
    finally:
        db.close()
    counts = {}
    for item in applied:
        counts[item["batch"]] = counts.get(item["batch"], 0) + 1
    print(json.dumps({"status": "PASS", "applied": len(applied), "byBatch": counts}, sort_keys=True))


if __name__ == "__main__":
    main()
