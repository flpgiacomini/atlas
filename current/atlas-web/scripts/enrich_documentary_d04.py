#!/usr/bin/env python3
"""Documentary pass D04: date four foundational vehicles from museum accession records.

These four sit at the origin of the industry and were unreachable in the product:
every projection of the Atlas filters by year, and none of them carried a date.
They were not short of sources — each is already backed by The Henry Ford, an
independent museum — only of the one thing that makes a record navigable.

The anchor is written where it belongs. Rather than invent a date predicate, the
pass dates the sourced relation that already exists: the Cadillac was
manufactured by Cadillac from 1903, the Curved Dash was marketed under
Oldsmobile from 1901 to 1907. That pays down the temporal debt and the
`valid_from` debt with the same edit, and it keeps the claim graph as it was.

What the museum records support is a year, not a day, and the precision says so.
Two candidates were dropped rather than guessed: the National Museum of
Australia returns HTTP 403 for both Holden pages, and the Ford Model N sits
behind a viewer that serves no readable record. An unread source gets no
locator, so the Holden 48-215 and the Model N stay undated and in the queue.

Idempotent: re-running writes the same values.
"""
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
BATCH = "D04"
NOW = "2026-08-31T15:00:00+00:00"

CURVED_DASH_QUOTE = "Oldsmobile built more than 19,000 Curved Dash models between 1901 and 1907"

RECORDS = {
    "Ford Quadricycle": {
        "description": (
            "Primeiro automóvel construído por Henry Ford. O exemplar preservado pelo museu The "
            "Henry Ford, sob o número de inventário 00.2.93, é datado de 1896, e a mesma ficha de "
            "acervo registra que Ford vendeu o Quadricycle ainda no fim daquele ano. O veículo "
            "antecede em sete anos a fundação da Ford Motor Company."
        ),
        "dates": {"designed_by": {"from": "1896", "precision": "year"}},
        "evidence": {
            "1896 Ford Quadricycle Runabout": {
                "*": {
                    "locator": {"inventory_number": "00.2.93", "section": "Overview", "object_date": "1896"},
                    "excerpt": "1896 Ford Quadricycle Runabout, First Car Built by Henry Ford",
                    "evidence_type": "collection_record",
                },
            },
        },
    },
    "Oldsmobile Curved Dash": {
        "description": (
            "Automóvel leve e barato que a Oldsmobile produziu entre 1901 e 1907. O museu The Henry "
            "Ford registra mais de 19 mil unidades construídas nesse intervalo, descreve o modelo "
            "como o primeiro carro americano fabricado em grande número e o aponta como mais "
            "vendido nos Estados Unidos entre 1902 e 1905. É esse intervalo de produção que data a "
            "comercialização sob a marca Oldsmobile."
        ),
        # Só a comercialização recebe o intervalo. O desenvolvimento por Ransom E. Olds
        # antecede a produção, e datá-lo de 1901 afirmaria mais do que a fonte diz.
        "dates": {"marketed_under": {"from": "1901", "until": "1907", "precision": "year"}},
        "evidence": {
            "The Curved Dash Oldsmobile": {
                "marketed_under": {
                    "locator": {"set": "The Curved Dash Oldsmobile", "section": "Toy Automobile, 1903-1905"},
                    "excerpt": CURVED_DASH_QUOTE,
                    "evidence_type": "collection_record",
                },
                "developed_by": {
                    "locator": {"set": "The Curved Dash Oldsmobile", "section": "Man and Woman in Curved-Dash Oldsmobile, 1901"},
                    "excerpt": CURVED_DASH_QUOTE,
                    "evidence_type": "collection_record",
                },
            },
        },
    },
    "Cadillac Runabout (1903)": {
        "description": (
            "Primeiro modelo de série da Cadillac Motor Car Company, empresa que Henry Leland "
            "formou em 1902 a partir do que restou da Henry Ford Company. O exemplar do museu The "
            "Henry Ford, número de inventário 29.509.1, é datado de 1903, e é por esse registro que "
            "a fabricação sob a marca fica situada no tempo."
        ),
        "dates": {"manufactured_by": {"from": "1903", "precision": "year"}},
        "evidence": {
            "1903 Cadillac Runabout": {
                "*": {
                    "locator": {"inventory_number": "29.509.1", "section": "Overview", "object_date": "1903"},
                    "excerpt": "Henry Leland formed Cadillac Motor Car Company in 1902 from the remains of the Henry Ford Company",
                    "evidence_type": "collection_record",
                },
            },
        },
    },
    "Ford Model A (1903)": {
        "description": (
            "Primeiro produto da Ford Motor Company, fundada em 1903. O museu The Henry Ford "
            "descreve o Model A como convencional para os padrões da época e data em 1903 o "
            "exemplar de seu acervo, registrado sob o número de inventário 00.136.137. É por esse "
            "registro que a fabricação pela Ford fica situada no tempo."
        ),
        "dates": {"manufactured_by": {"from": "1903", "precision": "year"}},
        "evidence": {
            "1903 Ford Model A Runabout": {
                "*": {
                    "locator": {"inventory_number": "00.136.137", "section": "Overview", "object_date": "1903"},
                    "excerpt": "The new company's first product, the Model A, was conventional by the standards of the day",
                    "evidence_type": "collection_record",
                },
            },
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
        """
        SELECT DISTINCT st.id AS statement_id, p.name AS predicate
        FROM statement st JOIN predicate p ON p.id = st.predicate_id
        WHERE st.subject_entity_id = ? ORDER BY st.id
        """,
        (entity_id,),
    ).fetchall()


def evidence_rows(db, entity_id):
    return db.execute(
        """
        SELECT DISTINCT e.id AS evidence_id, p.name AS predicate, s.title AS source_title
        FROM statement st
        JOIN predicate p ON p.id = st.predicate_id
        JOIN claim c ON c.statement_id = st.id
        JOIN claim_evidence ce ON ce.claim_id = c.id
        JOIN evidence e ON e.id = ce.evidence_id
        JOIN source s ON s.id = e.source_id
        WHERE st.subject_entity_id = ? ORDER BY e.id
        """,
        (entity_id,),
    ).fetchall()


def main():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    dated = touched = skipped = 0
    try:
        for name, record in RECORDS.items():
            entity_id, metadata_json = entity_row(db, name)

            for row in statement_rows(db, entity_id):
                window = record["dates"].get(row["predicate"])
                if not window:
                    continue
                db.execute(
                    """UPDATE statement SET valid_from=?, valid_from_precision=?,
                       valid_until=?, valid_until_precision=?, updated_at=? WHERE id=?""",
                    (
                        window["from"], window["precision"],
                        window.get("until"), window["precision"] if window.get("until") else None,
                        NOW, row["statement_id"],
                    ),
                )
                dated += 1

            for row in evidence_rows(db, entity_id):
                by_source = record["evidence"].get(row["source_title"])
                if not by_source:
                    skipped += 1
                    continue
                spec = by_source.get(row["predicate"]) or by_source.get("*")
                if not spec:
                    skipped += 1
                    continue
                db.execute(
                    "UPDATE evidence SET locator_json=?, excerpt=?, evidence_type=?, notes=? WHERE id=?",
                    (
                        json.dumps(spec["locator"], ensure_ascii=False, sort_keys=True),
                        spec["excerpt"],
                        spec["evidence_type"],
                        f"Passagem documental {BATCH}; ficha de acervo conferida na fonte em 2026-08-31.",
                        row["evidence_id"],
                    ),
                )
                touched += 1

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
        "evidenceUpdated": touched, "leftUnverified": skipped,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
