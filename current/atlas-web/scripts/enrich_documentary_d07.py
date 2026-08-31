#!/usr/bin/env python3
"""Documentary pass D07: two concept-to-production cars, dated and confronted.

The Cadillac Cyclone and the Škoda 1000 MB spoke only through General Motors and
Škoda Auto, and neither carried a date. Both now have a second voice.

The Audrain Auto Museum dates the Cyclone to 1959 and describes, in its own
words, the proximity sensors, the vapour-silvered canopy and the sliding doors —
so the museum confirms not only the year but the technology the Atlas already
claimed. Český rozhlas, the Czech public broadcaster, places the 1000 MB in 1964
at Mladá Boleslav, which puts a public-service institution beside the
manufacturer on a car that was itself a state-industry product.

Two candidates were tried and dropped. The Lincoln Futura is not in the Audrain's
GM exhibit — it is a Ford — and nothing else reachable dates it, so it stays in
the queue rather than borrowing a source that does not mention it.

Idempotent: statement updates rewrite the same values and the inserts are
INSERT OR IGNORE over deterministic ids.
"""
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
BATCH = "D07"
NOW = "2026-08-31T21:00:00+00:00"

CYCLONE_QUOTE = (
    "Introduced in 1959, the Cadillac Cyclone prototype was engineered to act as a "
    "'laboratory on wheels.'"
)
CYCLONE_SENSOR_QUOTE = (
    "The large black nose cones which project forward from the front of the car act as "
    "proximity sensors."
)
SKODA_QUOTE = "představenou v roce 1964 pod názvem Škoda 1000 MB"
SKODA_ARTICLE = "Rok 1964: Motor dáme dozadu. Škoda 1000 MB a její převratné novinky"


def stable_uuid7(seed: str) -> str:
    raw = bytearray(hashlib.sha256(f"atlas-documentary-d07:{seed}".encode()).digest()[:16])
    raw[6] = (raw[6] & 0x0F) | 0x70
    raw[8] = (raw[8] & 0x3F) | 0x80
    h = raw.hex()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


RECORDS = {
    "Cadillac Cyclone": {
        "description": (
            "Protótipo apresentado pela Cadillac em 1959 e concebido como um laboratório sobre "
            "rodas. O Audrain Auto Museum registra os grandes cones pretos que se projetam à frente "
            "e funcionam como sensores de proximidade, a bolha única revestida internamente com "
            "prata vaporizada para proteger os ocupantes da radiação ultravioleta e as portas que, "
            "ao toque de um botão, abriam deslizando para trás."
        ),
        "dates": {"marketed_under": {"from": "1959", "precision": "year"}},
        "confront": [
            {
                "predicate": "marketed_under",
                "source": "audrain-cyclone",
                "locator": {"section": "Styling the Future", "quote": "Introduced in 1959"},
                "excerpt": CYCLONE_QUOTE,
                "evidence_type": "explicit_statement",
                "note": (
                    "Confronto independente da data: o museu situa a apresentação do protótipo em "
                    "1959, fora do arquivo da General Motors."
                ),
            },
            {
                "predicate": "uses_technology",
                "object_like": "Alerta",
                "source": "audrain-cyclone",
                "locator": {"section": "Styling the Future", "quote": "act as proximity sensors"},
                "excerpt": CYCLONE_SENSOR_QUOTE,
                "evidence_type": "explicit_statement",
                "note": (
                    "Confronto independente da tecnologia: o museu descreve os cones dianteiros "
                    "como sensores de proximidade, sustentando a afirmação sem depender da "
                    "Cadillac."
                ),
            },
        ],
    },
    "ŠKODA 1000 MB": {
        "description": (
            "Automóvel apresentado em 1964 pela fábrica de Mladá Boleslav, segundo a rádio pública "
            "tcheca Český rozhlas. A mudança técnica central do projeto foi levar o motor para trás, "
            "com tração traseira, acompanhada de carroceria autoportante e de bloco de motor em "
            "alumínio fundido sob pressão."
        ),
        "dates": {"marketed_under": {"from": "1964", "precision": "year"}},
        "confront": [
            {
                "predicate": "marketed_under",
                "source": "cesky-rozhlas-1000mb",
                "locator": {"article": SKODA_ARTICLE, "section": "abertura"},
                "excerpt": SKODA_QUOTE,
                "evidence_type": "explicit_statement",
                "note": (
                    "Confronto independente da data: a rádio pública tcheca situa a apresentação do "
                    "1000 MB em 1964. A emissora não pertence à Škoda Auto nem ao grupo que a "
                    "controla."
                ),
            },
        ],
    },
}

SOURCES = {
    "audrain-cyclone": {
        "title": "1959 Cadillac Cyclone",
        "publisher": "Audrain Auto Museum",
        "url": "https://www.audrainautomuseum.org/styling-the-future/1959-cadillac-cyclone",
        "source_type": "museum",
        "language": "en",
    },
    "cesky-rozhlas-1000mb": {
        "title": SKODA_ARTICLE,
        "publisher": "Český rozhlas Plus",
        "url": "https://plus.rozhlas.cz/rok-1964-motor-dame-dozadu-skoda-1000-mb-a-jeji-prevratne-novinky-7565255",
        "source_type": "public_broadcaster",
        "language": "cs",
    },
}


def entity_row(db, name):
    row = db.execute("SELECT id, metadata_json FROM entity WHERE canonical_name=?", (name,)).fetchone()
    if not row:
        raise ValueError(f"Entidade ausente: {name}")
    return row


def statement_rows(db, entity_id):
    return db.execute(
        """SELECT st.id AS statement_id, p.name AS predicate, st.object_text,
                  (SELECT canonical_name FROM entity WHERE id = st.object_entity_id) AS object_name
           FROM statement st JOIN predicate p ON p.id = st.predicate_id
           WHERE st.subject_entity_id = ? ORDER BY st.id""",
        (entity_id,),
    ).fetchall()


def pick_statement(rows, plan):
    """Resolve which statement a confrontation attaches to.

    A predicate can appear more than once on an entity — the Cyclone claims three
    technologies — so a plan that targets one of them says which by naming part
    of the object. Anything ambiguous is a mistake in the batch, not something to
    resolve by picking the first match.
    """
    matches = [r for r in rows if r["predicate"] == plan["predicate"]]
    if fragment := plan.get("object_like"):
        matches = [r for r in matches if fragment.lower() in str(r["object_text"] or r["object_name"] or "").lower()]
    if len(matches) != 1:
        raise ValueError(f"alvo ambíguo ou ausente para {plan['predicate']}: {len(matches)} statements")
    return matches[0]["statement_id"]


def confront(db, name, statement_id, plan):
    meta = SOURCES[plan["source"]]
    source_id = stable_uuid7(f"source:{meta['url']}")
    db.execute(
        """INSERT OR IGNORE INTO source
           (id,source_type,title,author,publisher,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at)
           VALUES (?,?,?,?,?,?,?,?,'specialist','{}',?,?,?)""",
        (source_id, meta["source_type"], meta["title"], meta.get("author"), meta["publisher"],
         meta["url"], NOW, meta.get("language"),
         f"Fonte independente introduzida na passagem {BATCH}.", NOW, NOW),
    )
    seed = f"{name}:{plan['predicate']}:{plan.get('object_like','*')}:{meta['url']}"
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
    dated = confronted = 0
    try:
        for name, record in RECORDS.items():
            entity_id, metadata_json = entity_row(db, name)
            rows = statement_rows(db, entity_id)
            by_predicate = {}
            for row in rows:
                by_predicate.setdefault(row["predicate"], []).append(row["statement_id"])

            for predicate, window in record["dates"].items():
                targets = by_predicate.get(predicate) or []
                if len(targets) != 1:
                    raise ValueError(f"{name}: {predicate} tem {len(targets)} statements")
                db.execute(
                    """UPDATE statement SET valid_from=?, valid_from_precision=?,
                       valid_until=?, valid_until_precision=?, updated_at=? WHERE id=?""",
                    (window["from"], window["precision"], window.get("until"),
                     window["precision"] if window.get("until") else None, NOW, targets[0]),
                )
                dated += 1

            for plan in record.get("confront", []):
                confront(db, name, pick_statement(rows, plan), plan)
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
        "independentClaimsAdded": confronted,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
