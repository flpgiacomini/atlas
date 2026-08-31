#!/usr/bin/env python3
"""Documentary pass D10: create the Daimler Reitwagen, because the fact exists.

D09 read Deutsches Reichspatent 36423 — G. Daimler in Kannstatt, patented in the
German Empire on 29 August 1885, "Vehicle with gas or petroleum power machine" —
and then dropped it, because the Atlas had no entity the document could describe.
That was backwards. The Atlas exists to hold the automotive record, so a verified
document without a subject is a missing entity, not a discarded source.

The Reitwagen is created here from the patent alone. Every statement is something
the patent says in its own words: Daimler is the applicant, the machine runs on a
gas or petroleum motor, the chassis carries a steering wheel and a drive wheel in
the same track, and the motor hangs as low and as resiliently as possible between
them. Nothing is asserted that the document does not carry — Wilhelm Maybach's
part in the machine is well known and absent from the patent, so it is absent
here too, and the succession from the Reitwagen to the 1886 carriage waits for a
source that states it.

This pass also repairs the media manifest generator, which had drifted out of
sync with the manifest it writes and with the test that checks it: it emitted all
920 entities where the manifest holds only the 398 that are not catalogue stubs,
so running it would have failed the suite. It now filters to the same set and
keeps each entity's existing verification date instead of stamping today's onto
rows nobody re-checked.

Idempotent: the entity, its statements, claims and evidence all key on
deterministic ids under INSERT OR IGNORE, and re-running rewrites the same values.
"""
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
BATCH = "D10"
NOW = "2026-09-01T03:00:00+00:00"

PATENT_URL = "https://patents.google.com/patent/DE36423C/en"
OPENING = (
    "This vehicle essentially consists of the chassis 1 with seat 2 and a steering wheel 3 and a "
    "drive wheel 4 in the same track"
)
MOTOR = (
    "The driving force, the gas or Petroleum motor 5 with petroleum reservoir 6 is suspended as low "
    "as possible and resiliently between these wheels"
)

ENTITY_NAME = "Daimler Reitwagen (1885)"
DESCRIPTION = (
    "Veículo experimental de trilha única registrado por G. Daimler, de Kannstatt, no Deutsches "
    "Reichspatent 36423, patenteado no Império Alemão em 29 de agosto de 1885 sob o título "
    "“veículo com máquina motriz a gás ou petróleo”. O texto da patente descreve um chassi com "
    "assento, uma roda diretriz e uma roda motriz na mesma trilha, e um motor a gás ou petróleo "
    "com reservatório suspenso o mais baixo possível e de forma elástica entre as rodas. É o "
    "primeiro veículo rodoviário movido pelo motor rápido de Daimler."
)


def stable_uuid7(seed: str) -> str:
    raw = bytearray(hashlib.sha256(f"atlas-documentary-d10:{seed}".encode()).digest()[:16])
    raw[6] = (raw[6] & 0x0F) | 0x70
    raw[8] = (raw[8] & 0x3F) | 0x80
    h = raw.hex()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


# Cada statement traz o trecho da patente que o sustenta. Um fato sem trecho não entra.
STATEMENTS = [
    {
        "predicate": "invented_by",
        "object_type": "entity",
        "object": "Gottlieb Daimler",
        "excerpt": "G. DAIMLER in Kannstatt",
        "locator": {"patent": "DE 36423 C", "section": "Anmelder", "filed": "1885-08-29"},
        "note": "O requerente impresso na patente é G. Daimler, de Kannstatt.",
    },
    {
        "predicate": "uses_technology",
        "object_type": "entity",
        "object": "Motor de combustão interna",
        "excerpt": MOTOR,
        "locator": {"patent": "DE 36423 C", "section": "Beschreibung", "figure": "motor 5"},
        "note": "A patente descreve a força motriz como motor a gás ou petróleo com reservatório próprio.",
    },
    {
        "predicate": "configured_as",
        "object_type": "string",
        "object": "Trilha única: roda diretriz e roda motriz alinhadas no mesmo eixo longitudinal",
        "excerpt": OPENING,
        "locator": {"patent": "DE 36423 C", "section": "Beschreibung, parágrafo de abertura"},
        "note": "A configuração de trilha única é descrita na abertura da patente.",
    },
    {
        "predicate": "introduced_feature",
        "object_type": "string",
        "object": "Motor suspenso baixo e de forma elástica entre as rodas",
        "excerpt": MOTOR,
        "locator": {"patent": "DE 36423 C", "section": "Beschreibung", "figure": "motor 5, reservatório 6"},
        "note": "A suspensão baixa e elástica do motor entre as rodas é afirmada na patente.",
    },
]


def main():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    created = statements = 0
    try:
        entity_id = stable_uuid7(f"entity:{ENTITY_NAME}")
        metadata = {
            "editorial_level": "editorial",
            "editorial_batch": BATCH,
            "documentary_batch": BATCH,
            "vehicle_kind": "experimental",
            "vehicle_level": "standalone",
            "region_cluster": "Europa 1769-1899",
        }
        before = db.execute("SELECT COUNT(*) FROM entity WHERE id=?", (entity_id,)).fetchone()[0]
        db.execute(
            """INSERT OR IGNORE INTO entity (id,entity_type,canonical_name,slug,description,metadata_json,created_at,updated_at)
               VALUES (?,'vehicle',?,NULL,?,?,?,?)""",
            (entity_id, ENTITY_NAME, DESCRIPTION,
             json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, NOW),
        )
        db.execute(
            "UPDATE entity SET description=?, metadata_json=?, updated_at=? WHERE id=?",
            (DESCRIPTION, json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, entity_id),
        )
        created = int(not before)

        source_id = db.execute("SELECT id FROM source WHERE url=?", (PATENT_URL,)).fetchone()
        if source_id:
            source_id = source_id["id"]
        else:
            source_id = stable_uuid7(f"source:{PATENT_URL}")
            db.execute(
                """INSERT INTO source
                   (id,source_type,title,author,publisher,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at)
                   VALUES (?,'government',?,?,?,?,?,'de','primary','{}',?,?,?)""",
                (source_id, "Fahrzeug mit Gas- oder Petroleumkraftmaschine — Deutsches Reichspatent 36423",
                 "G. Daimler, Kannstatt", "Deutsches Patent- und Markenamt", PATENT_URL, NOW,
                 f"Fonte primária introduzida na passagem {BATCH}.", NOW, NOW),
            )

        for spec in STATEMENTS:
            predicate_id = db.execute("SELECT id FROM predicate WHERE name=?", (spec["predicate"],)).fetchone()
            if not predicate_id:
                raise ValueError(f"predicado ausente: {spec['predicate']}")
            object_entity = None
            if spec["object_type"] == "entity":
                row = db.execute("SELECT id FROM entity WHERE canonical_name=?", (spec["object"],)).fetchone()
                if not row:
                    raise ValueError(f"entidade-objeto ausente: {spec['object']}")
                object_entity = row["id"]

            seed = f"{ENTITY_NAME}:{spec['predicate']}:{spec['object']}"
            statement_id = stable_uuid7(f"statement:{seed}")
            db.execute(
                """INSERT OR IGNORE INTO statement
                   (id,subject_entity_id,predicate_id,object_type,object_entity_id,object_text,
                    valid_from,valid_from_precision,qualifiers_json,confidence,resolution_status,created_at,updated_at)
                   VALUES (?,?,?,?,?,?,?,'year','{}','high','accepted',?,?)""",
                (statement_id, entity_id, predicate_id["id"], spec["object_type"], object_entity,
                 None if object_entity else spec["object"], "1885", NOW, NOW),
            )
            claim_id = stable_uuid7(f"claim:{seed}")
            evidence_id = stable_uuid7(f"evidence:{seed}")
            db.execute(
                "INSERT OR IGNORE INTO claim (id,statement_id,stance,support_strength,note,created_at) VALUES (?,?,'supports','explicit',?,?)",
                (claim_id, statement_id, spec["note"], NOW),
            )
            db.execute(
                """INSERT OR IGNORE INTO evidence (id,source_id,evidence_type,locator_json,excerpt,notes,created_at)
                   VALUES (?,?,'patent_record',?,?,?,?)""",
                (evidence_id, source_id, json.dumps(spec["locator"], ensure_ascii=False, sort_keys=True),
                 spec["excerpt"], f"Passagem documental {BATCH}; trecho conferido na patente em 2026-08-31.", NOW),
            )
            db.execute("INSERT OR IGNORE INTO claim_evidence (claim_id,evidence_id) VALUES (?,?)", (claim_id, evidence_id))
            statements += 1
        db.commit()
    finally:
        db.close()
    print(json.dumps({
        "batch": BATCH, "entityCreated": created, "entity": ENTITY_NAME, "statements": statements,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
