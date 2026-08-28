#!/usr/bin/env python3
"""Documentary pass D02: three race entries, verified source by source.

Same method as D01 — replace template prose, write real locators and excerpts —
but this batch also exercises what the verification is for. Reading the sources
turned up attributions the sources do not carry:

* The Porsche "50 years of the 917" article never names Siffert or Ahrens, yet
  two driven_by claims cited it. Racing Sports Cars states both drivers, so the
  statements survive; the false backing is removed.
* The Henry Ford photograph-album record never mentions the number 7, yet the
  start_number claim cited it. The museum's other page does state "#7 Panhard",
  so that evidence is re-pointed rather than deleted.

And what it cannot do: the Mercedes-Benz Public Archive page returns HTTP 403,
so its five evidence records are left exactly as they are. An unread source gets
no locator. They stay in the documentary debt, which is the honest record.

Idempotent: re-running rewrites the same values and re-checks the same removals.
"""
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
BATCH = "D02"
NOW = "2026-08-28T13:00:00+00:00"

RSC_1969 = "10.8.1969 | 1000 km Zeltweg | 29 | #009 | Siffert / Ahrens, Jr. | Karl Freiherr v. Wendt | 1st"
PORSCHE_917_QUOTE = (
    "The car managed to secure an overall victory in its very first year of competing in the "
    "1,000-kilometre race at Zeltweg, Austria in 1969."
)
PORSCHE_917_SECTION = "Unparalleled dominance in motorsport and a trendsetter for turbo technology"
RENAULT_SECTION = "Il y a 110 ans, Renault gagne le premier Grand Prix de l'Histoire"
THF_SET_SECTION = (
    "Panhard Race Car Driven by George Heath Winning the First Vanderbilt Cup Race, "
    "Long Island, New York, October 8, 1904"
)
THF_SET_QUOTE = (
    "His French-built #7 Panhard finished in 5 hours, 26 minutes, 45 seconds, for an average "
    "race speed of 52.2 mph."
)
THF_ALBUM_QUOTE = "This photo album documents the 1904 race, won by American driver George Heath in a French-built Panhard."

RECORDS = {
    "1969 Zeltweg — Porsche 917 — Siffert/Ahrens": {
        "description": (
            "Inscrição do Porsche 917 número 29, chassi 009, nos 1000 km de Zeltweg de 10 de agosto "
            "de 1969, conduzida por Jo Siffert e Kurt Ahrens Jr. para Karl Freiherr von Wendt. Foi a "
            "primeira vitória geral do 917, obtida ainda no ano de estreia do modelo em competição."
        ),
        "evidence": {
            "Porsche 917 - All Results": {
                "*": {
                    "locator": {"section": "Year: 1969", "table": "10.8.1969 — 1000 km Zeltweg", "row": RSC_1969},
                    "excerpt": RSC_1969,
                    "evidence_type": "results_table",
                },
            },
            "Porsche celebrates “50 years of the 917”": {
                "*": {
                    "locator": {"section": PORSCHE_917_SECTION},
                    "excerpt": PORSCHE_917_QUOTE,
                    "evidence_type": "explicit_statement",
                },
                "entry_status": {
                    "locator": {"section": PORSCHE_917_SECTION},
                    "excerpt": PORSCHE_917_QUOTE,
                    "evidence_type": "entailed_statement",
                },
            },
        },
        # The article never names either driver; Racing Sports Cars does.
        "drop": [("Porsche celebrates “50 years of the 917”", "driven_by")],
    },
    "1906 Grand Prix de l'A.C.F. #3A — Ferenc Szisz / Renault": {
        "description": (
            "Inscrição de Ferenc Szisz no Grand Prix de l'A.C.F. de 27 de junho de 1906, com o Renault "
            "Type AK de 13 litros e 66 kW (90 cv). Szisz cruzou a linha de chegada com 32 minutos de "
            "vantagem sobre o segundo colocado, na primeira prova disputada sob o nome de Grande Prêmio."
        ),
        "evidence": {
            "Il y a 110 ans, Renault gagne le premier Grand Prix de l’Histoire": {
                "*": {
                    "locator": {"section": RENAULT_SECTION},
                    "excerpt": "Ferenc Szisz, pilote expérimenté, remporta ce triomphe spectaculaire",
                    "evidence_type": "explicit_statement",
                },
                "entered_vehicle": {
                    "locator": {"section": RENAULT_SECTION},
                    "excerpt": "la deux places Type AK de 66 kW/90 ch d'une cylindrée de 13 litres",
                    "evidence_type": "explicit_statement",
                },
                "overall_position": {
                    "locator": {"section": RENAULT_SECTION},
                    "excerpt": "il franchit la ligne d'arrivée loin devant ses concurrents, affichant une avance de 32 minutes sur le deuxième pilote",
                    "evidence_type": "explicit_statement",
                },
                "entry_for_event": {
                    "locator": {"section": RENAULT_SECTION},
                    "excerpt": "Le 27 juin 1906",
                    "evidence_type": "explicit_statement",
                },
                "entry_status": {
                    "locator": {"section": RENAULT_SECTION},
                    "excerpt": "il franchit la ligne d'arrivée loin devant ses concurrents",
                    "evidence_type": "entailed_statement",
                },
            },
            # "French Grand Prix" (Mercedes-Benz Public Archive) is deliberately
            # absent: the page returns HTTP 403 and was not read.
        },
    },
    "1904 Vanderbilt Cup #7 — George Heath / Panhard": {
        "description": (
            "Inscrição número 7 de George Heath na primeira Vanderbilt Cup, disputada em Long Island, "
            "Nova York, em 8 de outubro de 1904. Heath venceu com um Panhard de fabricação francesa, "
            "cobrindo o percurso em 5 horas, 26 minutos e 45 segundos, a uma média de 52,2 mph."
        ),
        "evidence": {
            "The Vanderbilt Cup": {
                "*": {
                    "locator": {"section": THF_SET_SECTION},
                    "excerpt": THF_SET_QUOTE,
                    "evidence_type": "explicit_statement",
                },
                "entry_status": {
                    "locator": {"section": THF_SET_SECTION},
                    "excerpt": THF_SET_QUOTE,
                    "evidence_type": "entailed_statement",
                },
            },
            "Photograph Album, 1904 Vanderbilt Cup Race": {
                "*": {
                    "locator": {"section": "Overview", "inventory_number": "92.1.1774.336"},
                    "excerpt": THF_ALBUM_QUOTE,
                    "evidence_type": "collection_record",
                },
                "entry_status": {
                    "locator": {"section": "Overview", "inventory_number": "92.1.1774.336"},
                    "excerpt": THF_ALBUM_QUOTE,
                    "evidence_type": "entailed_statement",
                },
            },
        },
        # The album record never mentions the number; the museum's set page does.
        "repoint": [("Photograph Album, 1904 Vanderbilt Cup Race", "start_number", "The Vanderbilt Cup")],
    },
}


def source_id(db, title):
    row = db.execute("SELECT id FROM source WHERE title=?", (title,)).fetchone()
    if not row:
        raise ValueError(f"Fonte ausente: {title}")
    return row[0]


def entity_row(db, name):
    row = db.execute("SELECT id, metadata_json FROM entity WHERE canonical_name=?", (name,)).fetchone()
    if not row:
        raise ValueError(f"Entidade ausente: {name}")
    return row


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
        WHERE st.subject_entity_id = ?
        ORDER BY e.id
        """,
        (entity_id,),
    ).fetchall()


def main():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    touched = dropped = repointed = skipped = 0
    try:
        for name, record in RECORDS.items():
            entity_id, metadata_json = entity_row(db, name)

            for title, predicate, target in record.get("repoint", []):
                for row in evidence_rows(db, entity_id):
                    if row["source_title"] == title and row["predicate"] == predicate:
                        db.execute("UPDATE evidence SET source_id=? WHERE id=?", (source_id(db, target), row["evidence_id"]))
                        repointed += 1

            for title, predicate in record.get("drop", []):
                for row in evidence_rows(db, entity_id):
                    if row["source_title"] != title or row["predicate"] != predicate:
                        continue
                    claims = [r[0] for r in db.execute(
                        "SELECT claim_id FROM claim_evidence WHERE evidence_id=?", (row["evidence_id"],))]
                    db.execute("DELETE FROM claim_evidence WHERE evidence_id=?", (row["evidence_id"],))
                    for claim_id in claims:
                        remaining = db.execute(
                            "SELECT COUNT(*) FROM claim_evidence WHERE claim_id=?", (claim_id,)).fetchone()[0]
                        if not remaining:
                            db.execute("DELETE FROM claim WHERE id=?", (claim_id,))
                    db.execute("DELETE FROM evidence WHERE id=?", (row["evidence_id"],))
                    dropped += 1

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
                        f"Passagem documental {BATCH}; localizador e trecho conferidos na fonte em 2026-08-28.",
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
        "batch": BATCH, "entities": len(RECORDS), "evidenceUpdated": touched,
        "evidenceRepointed": repointed, "evidenceDropped": dropped,
        "leftUnverified": skipped,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
