#!/usr/bin/env python3
"""Resolve the residual C07-C17 queue after conservative automated matching."""

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
NOW = "2026-08-26T00:15:00+00:00"
AUDIT_URL = "https://github.com/flpgiacomini/atlas/blob/main/current/atlas-web/data/imports/atlas-curation/brands-c07-c17.research.json"
MANUAL = {
    "Birkin": ("Q4916492", "Birkin Cars — fabricante sul-africano de automóveis esportivos."),
    "Bognor": ("Q14157870", "Fabricante automotivo identificado no registro estruturado individual."),
    "Burton": ("Q1017103", "Fabricante automotivo identificado no registro estruturado individual."),
    "Deepal": ("Q112874951", "Marca chinesa de veículos de nova energia."),
    "Firefly": ("Q131548598", "Marca chinesa de automóveis elétricos pertencente à Nio."),
    "Harper Sports Cars": ("Q1250017", "Fabricante de automóveis esportivos identificado individualmente."),
    "Onvo": ("Q125967298", "Marca chinesa de veículos elétricos pertencente à Nio."),
    "Southern Cross": ("Q2304687", "Fabricante automotivo histórico identificado individualmente."),
    "UMM": ("Q164726", "Fabricante português de automóveis, atualmente extinto."),
    "Vemag": ("Q10389626", "Fabricante brasileiro de automóveis."),
    "VinFast": ("Q56660561", "Fabricante automotivo vietnamita."),
}


def slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def main() -> None:
    research = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    unresolved = [item["candidateName"] for item in research["records"] if item["status"] == "unresolved"]
    db = sqlite3.connect(DB)
    promoted = retained = 0
    try:
        audit_source_id = stable_uuid7("source:" + AUDIT_URL)
        db.execute("""INSERT INTO source(id,source_type,title,publisher,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at)
            VALUES(?,'dataset','C07-C17 unresolved identity audit','Projeto Atlas',?,'2026-08-26','pt-BR','C','{}',
            'Snapshot reprodutível das tentativas de correspondência; não comprova contribuição histórica e sustenta apenas retenção conservadora.',?,?)
            ON CONFLICT(id) DO UPDATE SET accessed_at=excluded.accessed_at,notes=excluded.notes,updated_at=excluded.updated_at""",
            (audit_source_id, AUDIT_URL, NOW, NOW))
        for name in unresolved:
            row = db.execute("SELECT id,metadata_json FROM entity WHERE canonical_name=? AND entity_type='brand'", (name,)).fetchone()
            if not row:
                raise ValueError(f"brand candidate not found: {name}")
            metadata = json.loads(row[1] or "{}")
            wave = metadata["wave"]
            batch = f"C{int(wave[1:]) + 5:02d}-{wave}"
            if name in MANUAL:
                qid, description = MANUAL[name]
                url = f"https://www.wikidata.org/wiki/{qid}"
                source_id = stable_uuid7("source:" + url)
                db.execute("""INSERT INTO source(id,source_type,title,publisher,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at)
                    VALUES(?,'structured_reference',?,'Wikidata contributors',?,'2026-08-26','en','B',?,
                    'Correspondência individual revisada no fechamento C07-C17.',?,?)
                    ON CONFLICT(id) DO UPDATE SET accessed_at=excluded.accessed_at,updated_at=excluded.updated_at""",
                    (source_id, name, url, json.dumps({"wikidata": qid}), NOW, NOW))
                decision, state = "promote-editorial", "approved_pending_v2_cut"
                promoted += 1
            else:
                source_id = audit_source_id
                description = (f"Marca preservada no catálogo do recorte {metadata.get('region_cluster', 'regional')}. "
                               "A campanha C07–C17 não obteve correspondência individual inequívoca; nenhuma contribuição "
                               "histórica adicional é publicada até nova evidência.")
                decision, state = "retain-catalog", "retained_catalog_after_review"
                retained += 1
            metadata.update({
                "curation_batch": batch, "curation_review": f"atlas:curation-review:{batch.lower()}-{slug(name)}",
                "curation_reviewed_at": "2026-08-26", "curation_decision": decision,
                "curation_source_ids": [source_id], "editorial_level": "catalog", "promotion_state": state,
                "verification_state": "source_backed" if decision == "promote-editorial" else "identity_unresolved_retained",
                "verified_at": "2026-08-26", "research_match_method": "manual-wikidata" if name in MANUAL else "unresolved-retention",
            })
            db.execute("UPDATE entity SET description=?,metadata_json=?,updated_at=? WHERE id=?",
                       (description, json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, row[0]))
        db.commit()
    except Exception:
        db.rollback(); raise
    finally:
        db.close()
    print(json.dumps({"status": "PASS", "resolved": len(unresolved), "promote": promoted, "retain": retained}, sort_keys=True))


if __name__ == "__main__":
    main()
