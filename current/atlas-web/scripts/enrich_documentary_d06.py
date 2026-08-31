#!/usr/bin/env python3
"""Documentary pass D06: a race car, a concept car and a supercar leave the queue.

Three anchors, two of them confronted by institutions that have no stake in the
manufacturers' accounts.

The Panhard that won the first Vanderbilt Cup was already sourced to The Henry
Ford and needed nothing but the date its own record carries. The Buick Y-Job and
the Lamborghini Miura were dated nowhere and sourced only to General Motors and
Lamborghini, so their dates could not be published as established. Both now
carry a second claim from outside: the Y-Job is entry 14 on the National
Historic Vehicle Register and documented into the Library of Congress under HAER
MI-417, and the Miura's Geneva debut is stated by the Audrain Auto Museum.

The Miura also produced a disagreement worth keeping rather than smoothing. The
Atlas credits the design to Marcello Gandini on Lamborghini's word; the museum
credits the body to Bertone, the house Gandini worked for. Both are recorded and
the museum evidence is attached only to what the museum actually says.

Idempotent: statement updates rewrite the same values and the inserts are
INSERT OR IGNORE over deterministic ids.
"""
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
BATCH = "D06"
NOW = "2026-08-31T19:00:00+00:00"

PANHARD_SECTION = (
    "Panhard Race Car Driven by George Heath Winning the First Vanderbilt Cup Race, "
    "Long Island, New York, October 8, 1904"
)
PANHARD_QUOTE = (
    "His French-built #7 Panhard finished in 5 hours, 26 minutes, 45 seconds, for an average "
    "race speed of 52.2 mph."
)
MIURA_QUOTE = (
    "At the 1966 Geneva Auto Show, Lamborghini unveiled the Miura, a sleek mid-engine supercar "
    "designed by Bertone."
)
YJOB_QUOTE = "This experimental Buick ushered in the modern 'concept car.'"


def stable_uuid7(seed: str) -> str:
    raw = bytearray(hashlib.sha256(f"atlas-documentary-d06:{seed}".encode()).digest()[:16])
    raw[6] = (raw[6] & 0x0F) | 0x70
    raw[8] = (raw[8] & 0x3F) | 0x80
    h = raw.hex()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


RECORDS = {
    "Panhard race car — 1904 Vanderbilt Cup": {
        "description": (
            "Automóvel de competição da Panhard & Levassor que George Heath conduziu à vitória na "
            "primeira Vanderbilt Cup, em Long Island, Nova York, em 8 de outubro de 1904. O museu "
            "The Henry Ford registra que o Panhard número 7, de fabricação francesa, completou o "
            "percurso em 5 horas, 26 minutos e 45 segundos, a uma média de 52,2 mph."
        ),
        "dates": {"manufactured_by": {"from": "1904", "precision": "year"}},
        "evidence": {
            "The Vanderbilt Cup": {
                "*": {
                    "locator": {"section": PANHARD_SECTION, "quote": "October 8, 1904"},
                    "excerpt": PANHARD_QUOTE,
                    "evidence_type": "collection_record",
                },
            },
        },
    },
    "Buick Y-Job": {
        "description": (
            "Concept car construído em 1938 para explorar antecipadamente forma, equipamentos e "
            "reação pública, sem intenção imediata de produção. Concebido por Harley Earl na GM "
            "Design, está inscrito no National Historic Vehicle Register sob o número 14 e "
            "documentado no Historic American Engineering Record da Library of Congress sob HAER "
            "MI-417, registro que o descreve como o Buick experimental que inaugurou o concept car "
            "moderno."
        ),
        "dates": {"marketed_under": {"from": "1938", "precision": "year"}},
        "evidence": {},
        "confront": {
            "predicate": "marketed_under",
            "source": {
                "title": "1938 Buick Y-Job — National Historic Vehicle Register No. 14",
                "publisher": "Hagerty Drivers Foundation",
                "url": "https://driversfoundation.org/register/16",
                "source_type": "institutional",
                "language": "en",
            },
            "locator": {
                "register": "National Historic Vehicle Register No. 14",
                "documentation": "HAER No. MI-417",
                "repository": "Library of Congress, Prints and Photographs Division",
            },
            "excerpt": YJOB_QUOTE,
            "evidence_type": "register_record",
            "note": (
                "Confronto independente: o registro nacional data o objeto de 1938 e o documenta "
                "junto à Library of Congress, fora do arquivo da General Motors. O registro não "
                "afirma que o Y-Job foi o primeiro concept car, apenas que inaugurou o concept car "
                "moderno."
            ),
        },
    },
    "Lamborghini Miura": {
        "description": (
            "Automóvel esportivo de motor central apresentado pela Lamborghini no Salão de Genebra "
            "de 1966, segundo o Audrain Auto Museum, que atribui a carroceria à Bertone. A "
            "Lamborghini credita o desenho a Marcello Gandini, que trabalhava naquela casa. O "
            "modelo levou ao automóvel de rua a arquitetura de motor central então restrita à "
            "competição."
        ),
        "dates": {"marketed_under": {"from": "1966", "precision": "year"}},
        "evidence": {},
        "confront": {
            "predicate": "marketed_under",
            "source": {
                "title": "1968 Lamborghini Miura",
                "publisher": "Audrain Auto Museum",
                "url": "https://www.audrainautomuseum.org/past-to-present-exhibit/1968%20Lamborghini%20Miura",
                "source_type": "museum",
                "language": "en",
            },
            "locator": {"section": "Past to Present exhibit", "quote": "At the 1966 Geneva Auto Show"},
            "excerpt": MIURA_QUOTE,
            "evidence_type": "explicit_statement",
            "note": (
                "Confronto independente da estreia: o museu situa a apresentação no Salão de "
                "Genebra de 1966 e atribui a carroceria à Bertone. A atribuição do desenho a "
                "Marcello Gandini permanece sustentada apenas pela Lamborghini; o museu credita a "
                "casa, não o indivíduo."
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


def confront(db, name, statement_id, plan):
    """Attach a second, independent claim to a statement that already exists."""
    meta = plan["source"]
    source_id = stable_uuid7(f"source:{meta['url']}")
    db.execute(
        """INSERT OR IGNORE INTO source
           (id,source_type,title,author,publisher,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at)
           VALUES (?,?,?,?,?,?,?,?,'specialist','{}',?,?,?)""",
        (source_id, meta["source_type"], meta["title"], meta.get("author"), meta["publisher"],
         meta["url"], NOW, meta.get("language"),
         f"Fonte independente introduzida na passagem {BATCH}.", NOW, NOW),
    )
    seed = f"{name}:{plan['predicate']}:{meta['url']}"
    claim_id = stable_uuid7(f"claim:{seed}")
    evidence_id = stable_uuid7(f"evidence:{seed}")
    db.execute(
        "INSERT OR IGNORE INTO claim (id,statement_id,stance,support_strength,note,created_at) VALUES (?,?,'supports','explicit',?,?)",
        (claim_id, statement_id, plan["note"], NOW),
    )
    db.execute(
        """INSERT OR IGNORE INTO evidence (id,source_id,evidence_type,locator_json,excerpt,notes,created_at)
           VALUES (?,?,?,?,?,?,?)""",
        (evidence_id, source_id, plan["evidence_type"],
         json.dumps(plan["locator"], ensure_ascii=False, sort_keys=True), plan["excerpt"],
         f"Passagem documental {BATCH}; trecho conferido na fonte em 2026-08-31.", NOW),
    )
    db.execute("INSERT OR IGNORE INTO claim_evidence (claim_id,evidence_id) VALUES (?,?)", (claim_id, evidence_id))


def main():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    dated = touched = confronted = 0
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
                    continue
                db.execute(
                    "UPDATE evidence SET locator_json=?, excerpt=?, evidence_type=?, notes=? WHERE id=?",
                    (json.dumps(spec["locator"], ensure_ascii=False, sort_keys=True), spec["excerpt"],
                     spec["evidence_type"],
                     f"Passagem documental {BATCH}; localizador e trecho conferidos na fonte em 2026-08-31.",
                     row["evidence_id"]),
                )
                touched += 1

            if plan := record.get("confront"):
                confront(db, name, statements[plan["predicate"]], plan)
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
        "evidenceUpdated": touched, "independentClaimsAdded": confronted,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
