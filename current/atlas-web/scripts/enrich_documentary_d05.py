#!/usr/bin/env python3
"""Documentary pass D05: two more anchors and one confrontation.

The Gurgel BR-800 and the Panhard-Levassor Type M2E already carried independent
sources — a city government and a national museum — and still had no date, so
neither appeared in any temporal projection. Both are dated here from those same
sources, which is the cheapest kind of editorial work left in the queue: the
reading was already done, only the anchor was missing.

The Land Rover Series I is the opposite case. It was dated to 1948 and sourced
only to Land Rover's own press office, so under the confrontation rule its date
could not be published as established. Classic & Sports Car, an independent
specialist title, states the Amsterdam reveal outright, and that sentence is
attached here as a second claim on the statement that already existed — one
claim per source, as the model requires.

Four candidates were left alone rather than guessed. Quatro Rodas cannot be
fetched, the REME Museum and Hagerty return HTTP 403, and Autocar sits behind
HTTP 402, so the Gurgel Supermini, the Volkswagen Beetle and the Golf keep the
sources they have and stay in the queue. An unread source gets no locator.

Idempotent: statement updates rewrite the same values and the inserts are
INSERT OR IGNORE over deterministic ids.
"""
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
BATCH = "D05"
NOW = "2026-08-31T17:00:00+00:00"

GURGEL_QUOTE = (
    "Criou o Gurgel BR-800, primeiro automóvel 100% desenvolvido e fabricado no Brasil, "
    "que foi produzido entre 1988 e 1991."
)
LAND_ROVER_QUOTE = "It was a similar story with its reveal at the Amsterdam motor show, on 30 April 1948."


def stable_uuid7(seed: str) -> str:
    raw = bytearray(hashlib.sha256(f"atlas-documentary-d05:{seed}".encode()).digest()[:16])
    raw[6] = (raw[6] & 0x0F) | 0x70
    raw[8] = (raw[8] & 0x3F) | 0x80
    h = raw.hex()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


RECORDS = {
    "Gurgel BR-800": {
        "description": (
            "Automóvel compacto produzido pela Gurgel Motores entre 1988 e 1991. A Prefeitura de "
            "Rio Claro, cidade para onde a fábrica se transferiu em 1975, registra o BR-800 como o "
            "primeiro automóvel integralmente desenvolvido e fabricado no Brasil, criação de Amaral "
            "Gurgel. A empresa encerrou as atividades em 1996."
        ),
        "dates": {
            "manufactured_by": {"from": "1988", "until": "1991", "precision": "year"},
            "marketed_under": {"from": "1988", "until": "1991", "precision": "year"},
        },
        "evidence": {
            "Rio Claro celebra centenário de Amaral Gurgel": {
                "*": {
                    "locator": {"section": "Amaral Gurgel e a Gurgel Motores", "quote": "produzido entre 1988 e 1991"},
                    "excerpt": GURGEL_QUOTE,
                    "evidence_type": "explicit_statement",
                },
            },
            # Quatro Rodas não pôde ser lida nesta passagem e fica como estava.
        },
    },
    "Panhard-Levassor Type M2E": {
        "description": (
            "Automóvel fabricado pela Panhard & Levassor e conservado pelo Musée des Arts et "
            "Métiers sob o número de inventário 16715, cuja ficha data a fabricação de 1896. O "
            "catálogo do Conservatoire national des arts et métiers descreve seu motor de combustão "
            "interna, a transmissão e o sistema de refrigeração."
        ),
        "dates": {"manufactured_by": {"from": "1896", "precision": "year"}},
        "evidence": {
            "Automobile Panhard-Levassor type M2E": {
                "*": {
                    "locator": {"inventory_number": "Inv. 16715", "section": "Notice de l'objet", "field": "Date de fabrication"},
                    "excerpt": "Date de fabrication: 1896",
                    "evidence_type": "collection_record",
                },
            },
        },
    },
    "Land Rover Series I": {
        "description": (
            "Veículo utilitário apresentado pela Rover no Salão de Amsterdã em 30 de abril de 1948, "
            "segundo a revista Classic & Sports Car. A produção foi instalada na fábrica de Solihull "
            "e a marca Land Rover nasceu com este modelo, que deu origem a toda a linhagem posterior "
            "de utilitários da empresa."
        ),
        "dates": {"marketed_under": {"from": "1948", "precision": "year"}},
        "evidence": {},
        # A Land Rover falava sozinha sobre a própria estreia. Um segundo claim, com
        # fonte independente, passa a sustentar o mesmo statement.
        "confront": {
            "predicate": "marketed_under",
            "source": {
                "title": "1948's game changers: Land-Rover",
                "author": "Aaron McKay",
                "publisher": "Classic & Sports Car",
                "url": "https://www.classicandsportscar.com/features/1948s-game-changers-land-rover",
                "source_type": "specialized_journalism",
                "language": "en",
            },
            "locator": {"article": "1948's game changers: Land-Rover", "section": "Amsterdam reveal"},
            "excerpt": LAND_ROVER_QUOTE,
            "evidence_type": "explicit_statement",
            "note": (
                "Confronto independente da estreia: a revista situa a apresentação no Salão de "
                "Amsterdã em 30 de abril de 1948. A instalação da produção em Solihull permanece "
                "sustentada apenas pela Land Rover."
            ),
        },
    },
}


def entity_row(db, name):
    row = db.execute("SELECT id, metadata_json FROM entity WHERE canonical_name=?", (name,)).fetchone()
    if not row:
        raise ValueError(f"Entidade ausente: {name}")
    return row


def statement_rows(db, entity_id):
    return db.execute(
        """SELECT st.id AS statement_id, p.name AS predicate
           FROM statement st JOIN predicate p ON p.id = st.predicate_id
           WHERE st.subject_entity_id = ? ORDER BY st.id""",
        (entity_id,),
    ).fetchall()


def evidence_rows(db, entity_id):
    return db.execute(
        """SELECT DISTINCT e.id AS evidence_id, p.name AS predicate, s.title AS source_title
           FROM statement st
           JOIN predicate p ON p.id = st.predicate_id
           JOIN claim c ON c.statement_id = st.id
           JOIN claim_evidence ce ON ce.claim_id = c.id
           JOIN evidence e ON e.id = ce.evidence_id
           JOIN source s ON s.id = e.source_id
           WHERE st.subject_entity_id = ? ORDER BY e.id""",
        (entity_id,),
    ).fetchall()


def confront(db, name, statement_id, spec):
    """Attach a second, independent claim to a statement that already exists."""
    meta = spec["source"]
    source_id = stable_uuid7(f"source:{meta['url']}")
    db.execute(
        """INSERT OR IGNORE INTO source
           (id,source_type,title,author,publisher,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at)
           VALUES (?,?,?,?,?,?,?,?,'specialist','{}',?,?,?)""",
        (source_id, meta["source_type"], meta["title"], meta.get("author"), meta["publisher"],
         meta["url"], NOW, meta.get("language"),
         f"Fonte independente introduzida na passagem {BATCH}.", NOW, NOW),
    )
    seed = f"{name}:{spec['predicate']}:{meta['url']}"
    claim_id = stable_uuid7(f"claim:{seed}")
    evidence_id = stable_uuid7(f"evidence:{seed}")
    db.execute(
        "INSERT OR IGNORE INTO claim (id,statement_id,stance,support_strength,note,created_at) VALUES (?,?,'supports','explicit',?,?)",
        (claim_id, statement_id, spec["note"], NOW),
    )
    db.execute(
        """INSERT OR IGNORE INTO evidence (id,source_id,evidence_type,locator_json,excerpt,notes,created_at)
           VALUES (?,?,?,?,?,?,?)""",
        (evidence_id, source_id, spec["evidence_type"],
         json.dumps(spec["locator"], ensure_ascii=False, sort_keys=True), spec["excerpt"],
         f"Passagem documental {BATCH}; trecho conferido na fonte em 2026-08-31.", NOW),
    )
    db.execute("INSERT OR IGNORE INTO claim_evidence (claim_id,evidence_id) VALUES (?,?)", (claim_id, evidence_id))


def main():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    dated = touched = confronted = skipped = 0
    try:
        for name, record in RECORDS.items():
            entity_id, metadata_json = entity_row(db, name)
            statements = {row["predicate"]: row["statement_id"] for row in statement_rows(db, entity_id)}

            for predicate, window in record["dates"].items():
                if predicate not in statements:
                    raise ValueError(f"{name}: predicado ausente {predicate}")
                db.execute(
                    """UPDATE statement SET valid_from=?, valid_from_precision=?,
                       valid_until=?, valid_until_precision=?, updated_at=? WHERE id=?""",
                    (window["from"], window["precision"], window.get("until"),
                     window["precision"] if window.get("until") else None, NOW, statements[predicate]),
                )
                dated += 1

            for row in evidence_rows(db, entity_id):
                by_source = record["evidence"].get(row["source_title"])
                spec = (by_source.get(row["predicate"]) or by_source.get("*")) if by_source else None
                if not spec:
                    skipped += 1
                    continue
                db.execute(
                    "UPDATE evidence SET locator_json=?, excerpt=?, evidence_type=?, notes=? WHERE id=?",
                    (json.dumps(spec["locator"], ensure_ascii=False, sort_keys=True), spec["excerpt"],
                     spec["evidence_type"],
                     f"Passagem documental {BATCH}; localizador e trecho conferidos na fonte em 2026-08-31.",
                     row["evidence_id"]),
                )
                touched += 1

            if spec := record.get("confront"):
                confront(db, name, statements[spec["predicate"]], spec)
                confronted += 1

            metadata = json.loads(metadata_json) if metadata_json else {}
            metadata["documentary_batch"] = BATCH
            db.execute(
                "UPDATE entity SET description=?, metadata_json=?, updated_at=? WHERE id=?",
                (record["description"], json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, entity_id),
            )
        db.commit()
    finally:
        db.close()
    print(json.dumps({
        "batch": BATCH, "entities": len(RECORDS), "statementsDated": dated,
        "evidenceUpdated": touched, "independentClaimsAdded": confronted, "leftUnverified": skipped,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
