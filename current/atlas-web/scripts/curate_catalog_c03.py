#!/usr/bin/env python3
"""Apply CP19 C03 source records and reviewed decisions to the transition DB."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from enrich_people_batch_01 import stable_uuid7

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
NOW = "2026-08-25T18:00:00+00:00"

RECORDS = {
    "Lamborghini Marzal": {
        "review": "atlas:curation-review:c03-lamborghini-marzal",
        "description": "Protótipo de quatro lugares apresentado em 1967 que explorou uma interpretação radical do gran turismo Lamborghini. Sua consequência histórica é documentável na derivação do Espada, que levou parte da proposta formal e do conceito de quatro lugares à produção.",
        "source": ("manufacturer_archive", "Lamborghini History — Espada", "Automobili Lamborghini", "https://www.lamborghini.com/en-en/history/espada", "en", "A"),
    },
    "Alfa Romeo Carabo": {
        "review": "atlas:curation-review:c03-alfa-romeo-carabo",
        "description": "Protótipo desenhado por Marcello Gandini para a Bertone sobre a base mecânica do Alfa Romeo 33 Stradale e apresentado no Salão de Paris de 1968. A forma em cunha, a altura de 99 centímetros e as portas de abertura vertical materializaram uma ruptura documentada com o desenho curvilíneo anterior.",
        "source": ("manufacturer_archive", "The Carabo concept car on parade at Chantilly Arts & Elegance", "FCA Heritage / Stellantis", "https://www.media.stellantis.com/nl-nl/heritage-hub-italy/press/the-carabo-concept-car-on-parade-at-the-chantilly-arts-elegance-richard-mille-concours-d-elegance", "en", "A"),
    },
    "Holden Hurricane": {
        "review": "atlas:curation-review:c03-holden-hurricane",
        "description": "Primeiro automóvel-conceito projetado e produzido pelo departamento australiano de pesquisa e desenvolvimento da Holden, apresentado em 1969 como RD-001. O projeto registra a emergência de capacidade local de design e engenharia em Fishermans Bend, combinando carroceria em cunha e soluções experimentais sem intenção de produção.",
        "source": ("museum_publication", "NGV Magazine Jul–Aug 2022 — Holden Hurricane", "National Gallery of Victoria", "https://www.ngv.vic.gov.au/wp-content/uploads/2022/07/NGVMAG_JULAUG_35.pdf", "en", "A"),
    },
    "Lancia Stratos Zero": {
        "review": "atlas:curation-review:c03-lancia-stratos-zero",
        "description": "Protótipo em cunha criado pela Bertone a partir de desenho de Marcello Gandini e apresentado em 1970. A própria Lancia documenta o Stratos Zero como inspiração direta para o Stratos de 1971, estabelecendo uma ponte verificável entre show car radical, automóvel de competição e identidade visual posterior da marca.",
        "source": ("manufacturer_archive", "The journey towards the Lancia Design Day — brutal design", "Lancia / Stellantis", "https://www.media.stellantis.com/em-en/lancia/press/the-journey-towards-the-lancia-design-day-the-brutal-design-of-stratos-rally-037-and-delta", "en", "A"),
    },
    "Maserati Boomerang": {
        "review": "atlas:curation-review:c03-maserati-boomerang",
        "description": "Conceito criado por Giorgetto Giugiaro e produzido pela Italdesign, exibido inicialmente como maquete em Turim em 1971 e como automóvel funcional em Genebra em 1972. Construído em exemplar único sobre chassi e mecânica do Maserati Bora, condensou a fase experimental do desenho em cunha em um veículo registrável e operacional.",
        "source": ("manufacturer_archive", "Maserati Boomerang turns 50", "Maserati / Stellantis", "https://www.media.stellantis.com/uk-en/maserati/press/maserati-boomerang-turns-50", "en", "A"),
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
                VALUES(?,?,?,?,?,'2026-08-25',?,?,'{}','Fonte individual da revisão CP19 C03.',?,?)
                ON CONFLICT(id) DO UPDATE SET title=excluded.title,publisher=excluded.publisher,accessed_at=excluded.accessed_at,updated_at=excluded.updated_at""",
                (source_id, source_type, title, publisher, url, language, tier, NOW, NOW),
            )
            metadata = json.loads(row[1] or "{}")
            metadata.update({
                "curation_batch": "C03",
                "curation_review": record["review"],
                "curation_reviewed_at": "2026-08-25",
                "curation_decision": "promote-editorial",
                "curation_source_ids": [source_id],
                "promotion_state": "approved_pending_v2_cut",
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
    print(json.dumps({"batch": "C03", "reviewed": len(RECORDS), "promote": 5, "retain": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
