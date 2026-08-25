#!/usr/bin/env python3
"""Apply CP19 C02 source records and reviewed decisions to the transition DB."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from enrich_people_batch_01 import stable_uuid7

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
NOW = "2026-08-25T16:00:00+00:00"

RECORDS = {
    "Phantom Corsair": {
        "review": "atlas:curation-review:c02-phantom-corsair",
        "decision": "retain-catalog",
        "description": "Automóvel experimental de seis lugares preservado pelo National Automobile Museum como Phantom Corsair de 1938, associado a Bohman & Schwartz e Heinz. A identidade e a natureza one-off estão documentadas, mas a influência histórica atribuída ao projeto ainda não possui evidência individual suficiente para promoção editorial.",
        "source": ("museum_inventory", "Vehicle Inventory — 1938 Phantom Corsair Experimental", "National Automobile Museum", "https://automuseum.org/vehicle-inventory/", "en", "A"),
    },
    "Schlörwagen": {
        "review": "atlas:curation-review:c02-schlorwagen",
        "decision": "promote-editorial",
        "description": "Protótipo aerodinâmico desenvolvido na Aerodynamische Versuchsanstalt de Göttingen por Karl Schlör e construído pela Gebrüder Ludewig sobre base Mercedes-Benz 170 H. Medições registraram coeficiente de arrasto médio de 0,186, mas a sensibilidade a ventos laterais expôs o conflito entre eficiência aerodinâmica e estabilidade.",
        "source": ("research_archive", "Getting the Göttingen Egg rolling", "German Aerospace Center (DLR)", "https://www.dlr.de/en/media/publications/magazines/all-digital-magazines/dlr-magazine-173/getting-the-gottingen-egg-rolling", "en", "A"),
    },
    "Norman Timbs Special": {
        "review": "atlas:curation-review:c02-norman-timbs-special",
        "decision": "retain-catalog",
        "description": "Automóvel especial desenhado e construído pelo engenheiro Norman Timbs para uso pessoal. Uma fonte institucional o data como 1947, enquanto o catálogo legado registra 1948; até que documentação primária resolva a divergência e sustente sua contribuição para além da singularidade formal, o Atlas preserva o conflito e mantém o registro no catálogo.",
        "source": ("museum_report", "Newfields Annual Report 2014–2015 — Dream Cars", "Newfields / Indianapolis Museum of Art", "https://discovernewfields.org/application/files/5715/0811/4381/MAR_AnnualReport_2014-2015.pdf", "en", "B"),
    },
    "Nardi Bisiluro": {
        "review": "atlas:curation-review:c02-nardi-bisiluro",
        "decision": "promote-editorial",
        "description": "Protótipo assimétrico criado para as 24 Horas de Le Mans de 1955 por Mario Damonte, Carlo Mollino e Enrico Nardi. Dois volumes separados organizavam motor e transmissão de um lado e piloto e combustível do outro; o experimento competiu, abandonou após incidente aerodinâmico e foi doado ao museu em 1965.",
        "source": ("museum_catalog", "BISILURO DaMolNar 1955", "Museo Nazionale Scienza e Tecnologia Leonardo da Vinci", "https://www.museoscienza.org/besrv/sites/default/files/2025-06/Cartrella_Stampa_fatte_misura.pdf", "it", "A"),
    },
    "Golden Sahara II": {
        "review": "atlas:curation-review:c02-golden-sahara-ii",
        "decision": "promote-editorial",
        "description": "Custom car experimental desenvolvido por Jim Street e George Barris como plataforma para sistemas eletrônicos, com comandos inspirados em aeronaves, frenagem automática por sensores e pneus translúcidos iluminados da Goodyear. Sua relevância está na apresentação pública de automação e interfaces, não em autonomia equivalente à atual.",
        "source": ("corporate_archive", "World premiere of restored Golden Sahara II", "Goodyear", "https://www.goodyear.co.jp/press/2019/0318-213702.html", "ja", "A"),
    },
}


def main() -> None:
    db = sqlite3.connect(DB)
    try:
        for name, record in RECORDS.items():
            row = db.execute("SELECT id, metadata_json FROM entity WHERE canonical_name=?", (name,)).fetchone()
            if not row:
                raise ValueError(f"candidate not found: {name}")
            source_type, title, publisher, url, language, tier = record["source"]
            source_id = stable_uuid7("source:" + url)
            db.execute(
                """INSERT INTO source(id,source_type,title,publisher,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at)
                VALUES(?,?,?,?,?,'2026-08-25',?,?,'{}','Fonte individual da revisão CP19 C02.',?,?)
                ON CONFLICT(id) DO UPDATE SET title=excluded.title,publisher=excluded.publisher,accessed_at=excluded.accessed_at,updated_at=excluded.updated_at""",
                (source_id, source_type, title, publisher, url, language, tier, NOW, NOW),
            )
            metadata = json.loads(row[1] or "{}")
            metadata.update({
                "curation_batch": "C02",
                "curation_review": record["review"],
                "curation_reviewed_at": "2026-08-25",
                "curation_decision": record["decision"],
                "curation_source_ids": [source_id],
                "promotion_state": "approved_pending_v2_cut" if record["decision"] == "promote-editorial" else "retained_catalog_after_review",
                "editorial_level": "catalog",
                "verification_state": "source_backed",
                "verified_at": "2026-08-25",
            })
            db.execute(
                "UPDATE entity SET description=?, metadata_json=?, updated_at=? WHERE id=?",
                (record["description"], json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, row[0]),
            )
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    print(json.dumps({"batch": "C02", "reviewed": len(RECORDS), "promote": 3, "retain": 2}, ensure_ascii=False))


if __name__ == "__main__":
    main()
