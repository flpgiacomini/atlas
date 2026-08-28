#!/usr/bin/env python3
"""Documentary pass D01: replace template prose and give each evidence a real locator.

The migrated corpus is complete in structure and hollow in documentation. Its
descriptions were generated from the claim graph ("A documentação registra
condução por..."), and 488 of its 737 evidence records carry a marker announcing
that the locator was never written ("refine page/section locator during deep
curation"). Neither defect can be repaired downstream: migration/ is regenerated
from this database on every run, so the fix belongs here.

Each record in this batch is verified against the live source before being
written. A locator names where the assertion sits in the document; an excerpt
quotes it. Where the source supports an assertion without stating it verbatim,
the evidence is marked entailed rather than explicit instead of being dressed up.

Idempotent: re-running rewrites the same values.
"""
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
BATCH = "D01"
NOW = "2026-08-28T12:00:00+00:00"

ACO_SECTION = "1970 | The last two of seven 917s win the race"
ACO_QUOTE = (
    "Driving the last of the seven 917s (qualified in 14th position), Richard Attwood and "
    "Hans Herrmann (Porsche Konstruktionen Salzburg) took advantage of the carnage caused by "
    "the wet weather."
)
PORSCHE_SECTION = "Hans Herrmann and Richard Attwood reminisce about the race"
PORSCHE_QUOTE = (
    "Hans Herrmann and Richard Attwood crossed the finishing line first in the Porsche 917 KH "
    "from Porsche Salzburg with the start number 23."
)
PORSCHE_OPENING = (
    "On 14 June 1970, Porsche achieved its first overall victory there with the 580 hp 917 KH "
    "sports car."
)
RSC_ROW = "23 | #023 | Attwood / Herrmann | Porsche Konstruktionen K.G. | 1st"

RECORDS = {
    "1970 Le Mans #23 — Porsche 917 K 917-023 — Attwood/Herrmann": {
        "description": (
            "Inscrição número 23 das 24 Horas de Le Mans de 14 de junho de 1970: o Porsche 917 KH "
            "de chassi 023, conduzido por Hans Herrmann e Richard Attwood pela Porsche "
            "Konstruktionen Salzburg. Classificada em 14º no grid entre as sete unidades do 917 "
            "inscritas, aproveitou o desgaste provocado pela chuva e cruzou a linha de chegada em "
            "primeiro, dando à Porsche sua primeira vitória geral em Le Mans."
        ),
        "evidence": {
            "Racing Sports Cars": {
                "*": {
                    "locator": {
                        "section": "Year: 1970",
                        "table": "14.6.1970 — Le Mans 24 Hours",
                        "row": RSC_ROW,
                    },
                    "excerpt": RSC_ROW,
                    "evidence_type": "results_table",
                },
            },
            "Automobile Club de l'Ouest / 24 Hours of Le Mans": {
                "*": {
                    "locator": {"section": ACO_SECTION},
                    "excerpt": ACO_QUOTE,
                    "evidence_type": "explicit_statement",
                },
                "start_number": {
                    "locator": {"section": ACO_SECTION, "figure": "photo caption"},
                    "excerpt": "the winning car in 1970 (#23)",
                    "evidence_type": "explicit_statement",
                },
                # No source in this batch uses the word "classified"; each states
                # that the car finished and won. The status follows from that and
                # is recorded as entailed, not as something the source says.
                "entry_status": {
                    "locator": {"section": ACO_SECTION},
                    "excerpt": ACO_QUOTE,
                    "evidence_type": "entailed_statement",
                },
            },
            "Porsche AG": {
                "*": {
                    "locator": {"section": PORSCHE_SECTION},
                    "excerpt": PORSCHE_QUOTE,
                    "evidence_type": "explicit_statement",
                },
                "entry_for_event": {
                    "locator": {"section": "opening paragraph"},
                    "excerpt": PORSCHE_OPENING,
                    "evidence_type": "explicit_statement",
                },
                "entry_status": {
                    "locator": {"section": PORSCHE_SECTION},
                    "excerpt": PORSCHE_QUOTE,
                    "evidence_type": "entailed_statement",
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


def evidence_rows(db, entity_id):
    return db.execute(
        """
        SELECT DISTINCT e.id AS evidence_id, p.name AS predicate, s.publisher
        FROM statement st
        JOIN predicate p ON p.id = st.predicate_id
        JOIN claim c ON c.statement_id = st.id
        JOIN claim_evidence ce ON ce.claim_id = c.id
        JOIN evidence e ON e.id = ce.evidence_id
        JOIN source s ON s.id = e.source_id
        WHERE st.subject_entity_id = ?
        ORDER BY e.id
        """,
        (entity_id,),
    ).fetchall()


def main():
    db = sqlite3.connect(DB)
    db.execute("PRAGMA foreign_keys=ON")
    touched = unmapped = 0
    try:
        for name, record in RECORDS.items():
            entity_id, metadata_json = entity_row(db, name)
            for evidence_id, predicate, publisher in evidence_rows(db, entity_id):
                by_publisher = record["evidence"].get(publisher)
                if not by_publisher:
                    unmapped += 1
                    continue
                spec = by_publisher.get(predicate) or by_publisher.get("*")
                if not spec:
                    unmapped += 1
                    continue
                db.execute(
                    "UPDATE evidence SET locator_json=?, excerpt=?, evidence_type=?, notes=? WHERE id=?",
                    (
                        json.dumps(spec["locator"], ensure_ascii=False, sort_keys=True),
                        spec["excerpt"],
                        spec["evidence_type"],
                        f"Passagem documental {BATCH}; localizador e trecho conferidos na fonte em 2026-08-28.",
                        evidence_id,
                    ),
                )
                touched += 1
            metadata = json.loads(metadata_json) if metadata_json else {}
            metadata["documentary_batch"] = BATCH
            db.execute(
                "UPDATE entity SET description=?, metadata_json=?, updated_at=? WHERE id=?",
                (
                    record["description"],
                    json.dumps(metadata, ensure_ascii=False, sort_keys=True),
                    NOW,
                    entity_id,
                ),
            )
        db.commit()
    finally:
        db.close()
    print(json.dumps({"batch": BATCH, "entities": len(RECORDS), "evidenceUpdated": touched, "unmapped": unmapped}, ensure_ascii=False, sort_keys=True))
    if unmapped:
        raise SystemExit(f"{unmapped} evidence rows had no locator mapping")


if __name__ == "__main__":
    main()
