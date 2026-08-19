#!/usr/bin/env python3
"""Complete the Panhard-Levassor Type M2E record from the CNAM catalogue."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from enrich_people_batch_01 import stable_uuid7


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
NOW = "2026-08-19T12:00:00+00:00"
SOURCE_URL = "https://cnum.cnam.fr/pgi/redir.php?ident=M6118&onglet=c"
SUBJECT = "Panhard-Levassor Type M2E"


SUPPORT_ENTITIES = {
    "Transmissão do Panhard-Levassor Type M2E": (
        "component",
        "Conjunto mecânico documentado no Panhard-Levassor Type M2E de 1896. O catálogo do CNAM descreve caixa de velocidades com eixos paralelos, embreagem cônica, diferencial por engrenagens cônicas e correntes responsáveis por transmitir o movimento às rodas traseiras.",
        {"component_type": "transmission", "editorial_batch": "V01-M2E"},
    ),
    "Refrigeração do Panhard-Levassor Type M2E": (
        "component",
        "Sistema de refrigeração líquida documentado no Panhard-Levassor Type M2E de 1896. A água circulava por uma bomba acionada pelo contato de um rolete com o volante do motor, solução específica preservada na descrição técnica do catálogo do CNAM.",
        {"component_type": "cooling_system", "editorial_batch": "V01-M2E"},
    ),
}


RELATIONS = (
    ("uses_technology", "Motor de combustão interna", {"catalogue_page": 83, "specification": "motor bicilíndrico, 4 cv, 700 rpm"}),
    ("uses_component", "Transmissão do Panhard-Levassor Type M2E", {"catalogue_pages": [83, 84]}),
    ("uses_component", "Refrigeração do Panhard-Levassor Type M2E", {"catalogue_page": 83}),
)


def entity_id(db: sqlite3.Connection, name: str) -> str:
    row = db.execute("SELECT id FROM entity WHERE canonical_name=?", (name,)).fetchone()
    if not row:
        raise ValueError(f"Entidade ausente: {name}")
    return row[0]


def main() -> None:
    db = sqlite3.connect(DB)
    db.execute("PRAGMA foreign_keys=ON")
    try:
        for name, (entity_type, description, metadata) in SUPPORT_ENTITIES.items():
            db.execute(
                """INSERT INTO entity
                   (id,entity_type,canonical_name,slug,description,metadata_json,created_at,updated_at)
                   VALUES (?,?,?,NULL,?,?,?,?)
                   ON CONFLICT(id) DO UPDATE SET description=excluded.description,
                   metadata_json=excluded.metadata_json,updated_at=excluded.updated_at""",
                (
                    stable_uuid7(f"entity:{name}"),
                    entity_type,
                    name,
                    description,
                    json.dumps(metadata, ensure_ascii=False, sort_keys=True),
                    NOW,
                    NOW,
                ),
            )

        source_id = stable_uuid7(f"source:{SOURCE_URL}")
        db.execute(
            """INSERT INTO source
               (id,source_type,title,author,publisher,published_at,url,accessed_at,language,
                source_tier,zotero_key,external_ids_json,notes,created_at,updated_at)
               VALUES (?,'museum_catalogue','Catalogue du musée. Section DA, Transports sur route',
                       'Conservatoire national des arts et métiers',
                       'Conservatoire national des arts et métiers','1953',?,'2026-08-19','fr',
                       'A',NULL,'{}','Descrição técnica do item 16.715 nas páginas 83–84.',?,?)
               ON CONFLICT(id) DO UPDATE SET accessed_at=excluded.accessed_at,updated_at=excluded.updated_at""",
            (source_id, SOURCE_URL, NOW, NOW),
        )

        subject_id = entity_id(db, SUBJECT)
        statement_ids: list[str] = []
        for predicate, object_name, locator in RELATIONS:
            predicate_id = db.execute("SELECT id FROM predicate WHERE name=?", (predicate,)).fetchone()[0]
            object_id = entity_id(db, object_name)
            seed = f"{SUBJECT}:{predicate}:{object_name}:cnam-1953"
            statement_id = stable_uuid7(f"statement:{seed}")
            statement_ids.append(statement_id)
            db.execute(
                """INSERT OR IGNORE INTO statement
                   (id,subject_entity_id,predicate_id,object_type,object_entity_id,qualifiers_json,
                    confidence,resolution_status,created_at,updated_at)
                   VALUES (?,?,?,'entity',?,?, 'high','accepted',?,?)""",
                (statement_id, subject_id, predicate_id, object_id,
                 json.dumps({"editorial_batch": "V01-M2E", **locator}, ensure_ascii=False), NOW, NOW),
            )
            claim_id = stable_uuid7(f"claim:{seed}")
            evidence_id = stable_uuid7(f"evidence:{seed}")
            db.execute(
                "INSERT OR IGNORE INTO claim (id,statement_id,stance,support_strength,note,created_at) VALUES (?,?,'supports','explicit',?,?)",
                (claim_id, statement_id, "Relação derivada da descrição técnica individual do item 16.715.", NOW),
            )
            db.execute(
                """INSERT OR IGNORE INTO evidence
                   (id,source_id,evidence_type,locator_json,excerpt,notes,created_at)
                   VALUES (?,?,'catalogue_entry',?,NULL,?,?)""",
                (evidence_id, source_id, json.dumps(locator, ensure_ascii=False),
                 "Item 2, Panhard et Levassor type M2E, páginas impressas 83–84; sem reprodução extensa.", NOW),
            )
            db.execute("INSERT OR IGNORE INTO claim_evidence (claim_id,evidence_id) VALUES (?,?)", (claim_id, evidence_id))

        row = db.execute("SELECT metadata_json FROM entity WHERE id=?", (subject_id,)).fetchone()
        metadata = json.loads(row[0] or "{}")
        basis = set(metadata.get("description_basis_statement_ids", []))
        basis.update(statement_ids)
        metadata["description_basis_statement_ids"] = sorted(basis)
        metadata["editorial_batch"] = "V01-M2E"
        db.execute(
            "UPDATE entity SET metadata_json=?,updated_at=? WHERE id=?",
            (json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, subject_id),
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    print(json.dumps({"subject": SUBJECT, "relations_added": len(RELATIONS), "support_entities": len(SUPPORT_ENTITIES), "status": "ok"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
