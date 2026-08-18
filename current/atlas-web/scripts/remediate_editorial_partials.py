#!/usr/bin/env python3
"""Add source-supported relations for the residual editorial partials."""

import json
import sqlite3
from pathlib import Path

from enrich_people_batch_01 import add_statement, stable_uuid7

ROOT = Path(__file__).resolve().parents[1]

REMEDIATIONS = [
    ("BMW 3 Series", "https://www.press.bmwgroup.com/south-africa/article/detail/T0278716EN/after-35-years-the-bmw-3-series-sedan-rolls-off-the-production-line-at-bmw-group-plant-rosslyn-to-make-way-for-the-new-bmw-x3?language=en", ("manufactured_by", "entity", "BMW Group", None, None, None)),
    ("Benz Patent Motor Car Model 1", "https://mercedes-benz-publicarchive.com/marsClassic/en/instance/ko/Benz-patent-motor-car-Model-1.xhtml?oid=4376", ("designed_by", "entity", "Carl Benz", None, None, None)),
    ("Gurgel Supermini", "https://quatrorodas.abril.com.br/carros-classicos/gurgel-supermini/", ("manufactured_by", "entity", "Gurgel Motores S/A", None, None, None)),
    ("Mercedes 28/95 hp", "https://mercedes-benz-publicarchive.com/marsClassic/en/instance/ko/Mercedes-2895-hp-1914---1924.xhtml?oid=5916", ("manufactured_by", "entity", "Daimler-Motoren-Gesellschaft", None, None, None)),
    ("Panhard race car — 1904 Vanderbilt Cup", "https://www.thehenryford.org/collections/explore/sets/detail/the-vanderbilt-cup", ("manufactured_by", "entity", "Panhard & Levassor", None, None, None)),
    ("Peugeot Type 3", "https://www.media.stellantis.com/em-en/peugeot/press/peugeot-210-years-of-history-and-13-films-to-relive-it-all", ("marketed_under", "entity", "Peugeot", None, None, None)),
    ("Porsche 356", "https://newsroom.porsche.com/en/products/porsche-one-millionth-911-milestone-automotive-icon-sports-car-13737.html", ("manufactured_by", "entity", "Dr. Ing. h.c. F. Porsche AG", None, None, None)),
    ("Porsche 917 LH", "https://newsroom.porsche.com/en/2019/history/porsche-museum-50-years-917-special-exhibition-17184.html", ("manufactured_by", "entity", "Dr. Ing. h.c. F. Porsche AG", None, None, None)),
    ("Porsche Type 754 T7", "https://newsroom.porsche.com/en/history/porsche-911-evolutionary-history-754-901-ferry-porsche-14641.html", ("designed_by", "entity", "Ferdinand Alexander Porsche", None, None, None)),
    ("Renault Type AK Grand Prix", "https://be.media.renaultgroup.com/il-y-a-110-ans-renault-gagne-le-premier-grand-prix-de-lhistoire/", ("manufactured_by", "entity", "Renault Frères", None, None, None)),
    ("Land Rover Series I launch at Amsterdam Motor Show", "https://media.landrover.com/en-us/news/2018/01/land-rovers-70th-anniversary-begins-restoration-missing-original-4x4", ("involved", "entity", "Land Rover pre-production HUE 166", None, None, None)),
]


def main():
    db = sqlite3.connect(ROOT / "data" / "atlas.sqlite")
    db.execute("PRAGMA foreign_keys=ON")
    try:
        for subject, url, statement in REMEDIATIONS:
            row = db.execute("SELECT id FROM source WHERE url=? ORDER BY id LIMIT 1", (url,)).fetchone()
            if not row:
                raise ValueError(f"Fonte canônica ausente: {url}")
            add_statement(db, subject, row[0], statement)
        m2e_id = db.execute("SELECT id FROM entity WHERE canonical_name='Panhard-Levassor Type M2E'").fetchone()[0]
        db.execute("""UPDATE entity SET description=?,updated_at=? WHERE id=?""", (
            "Automóvel Panhard-Levassor fabricado em 1896 e preservado pelo Musée des Arts et Métiers sob o inventário 16715. O registro museológico destaca sua condição de produto de luxo e a combinação de construção aparentemente simples com inovações importantes para a época.",
            "2026-08-18T21:30:00+00:00", m2e_id))
        db.execute("""INSERT OR IGNORE INTO external_identifier(id,entity_id,scheme,value,url,created_at)
          VALUES (?,?,?,?,?,?)""", (stable_uuid7("external:Panhard-Levassor Type M2E:wikidata"), m2e_id, "wikidata", "Q119890021",
          "https://www.wikidata.org/wiki/Q119890021", "2026-08-18T21:30:00+00:00"))
        detail_url = "https://www.arts-et-metiers.net/musee/automobile-panhard-levassor-type-m2e"
        detail_source = stable_uuid7(f"source:{detail_url}")
        db.execute("""INSERT OR IGNORE INTO source
          (id,source_type,title,author,publisher,published_at,url,accessed_at,language,source_tier,zotero_key,external_ids_json,notes,created_at,updated_at)
          VALUES (?,'museum_collection','Automobile Panhard-Levassor type M2E',NULL,'Musée des Arts et Métiers',NULL,?,'2026-08-18','fr','A',NULL,'{}','Registro do objeto, data de fabricação e número de inventário.',?,?)""",
          (detail_source, detail_url, "2026-08-18T21:30:00+00:00", "2026-08-18T21:30:00+00:00"))
        statement_id = db.execute("""SELECT s.id FROM statement s JOIN predicate p ON p.id=s.predicate_id
          WHERE s.subject_entity_id=? AND p.name='manufactured_by'""", (m2e_id,)).fetchone()[0]
        claim_id = db.execute("SELECT id FROM claim WHERE statement_id=? ORDER BY id LIMIT 1", (statement_id,)).fetchone()[0]
        evidence_id = stable_uuid7("evidence:Panhard-Levassor Type M2E:museum-detail")
        db.execute("""INSERT OR IGNORE INTO evidence(id,source_id,evidence_type,locator_json,excerpt,notes,created_at)
          VALUES (?,?,'museum_record',?,NULL,?,?)""", (evidence_id, detail_source,
          json.dumps({"inventory_number":"16715","manufacture_date":"1896"}),
          "Registro museológico individual; sem reprodução de trecho protegido.", "2026-08-18T21:30:00+00:00"))
        db.execute("INSERT OR IGNORE INTO claim_evidence(claim_id,evidence_id) VALUES (?,?)", (claim_id, evidence_id))
        db.commit()
    except Exception:
        db.rollback(); raise
    finally:
        db.close()
    print(json.dumps({"relations_added": len(REMEDIATIONS), "museum_records_enriched": 1, "remaining_known_gap": "Panhard-Levassor Type M2E", "status": "ok"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
