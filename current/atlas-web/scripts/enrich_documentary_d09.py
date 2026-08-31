#!/usr/bin/env python3
"""Documentary pass D09: the founding patent, and a Ford dated by its museum.

The Benz Patent-Motorwagen is the Atlas's oldest vehicle and the whole product's
starting point, and every word about it came from the company that built it. The
fix was sitting in a public registry the whole time: Deutsches Reichspatent
37435, filed on 29 January 1886 by Benz & Co. of Mannheim. A patent filing is an
act of a third party — the manufacturer cannot backdate it — so it fixes the date
without the archive's help. The authored document gets the registry alongside
Mercedes-Benz's account of it; this batch does the same for Model 1 in the
migrated corpus.

The patent names Benz & Co. as applicant, not Carl Benz personally, and the note
says so. Attributing the design to the man remains the manufacturer's word.

The Ford Model N leaves the queue on The Henry Ford's accession record, 85.115.1,
which dates the object to 1906 and states what it sold for.

Daimler was tried and dropped. DE 36423 C covers the 1885 Reitwagen, a
single-track machine, and the Atlas has no entity for it; attaching it to the
1886 Motorized Carriage would credit that vehicle with a document that does not
describe it. The carriage stays sourced to Mercedes-Benz alone.

Idempotent: statement updates rewrite the same values, sources are reused when
their URL is already registered, and the inserts are INSERT OR IGNORE over
deterministic ids.
"""
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
BATCH = "D09"
NOW = "2026-09-01T01:00:00+00:00"

PATENT_QUOTE = (
    "The present construction aims to operate mainly light wagons and small ships, such as those "
    "used for the transport of 1 to 4 people."
)
MODEL_N_QUOTE = "At $500, it became the bestselling car in America"


def stable_uuid7(seed: str) -> str:
    raw = bytearray(hashlib.sha256(f"atlas-documentary-d09:{seed}".encode()).digest()[:16])
    raw[6] = (raw[6] & 0x0F) | 0x70
    raw[8] = (raw[8] & 0x3F) | 0x80
    h = raw.hex()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


SOURCES = {
    "dpma-patent-37435": {
        "title": "Fahrzeug mit Gasmotorenbetrieb — Deutsches Reichspatent 37435",
        "author": "Benz & Co., Mannheim",
        "publisher": "Deutsches Patent- und Markenamt",
        "url": "https://patents.google.com/patent/DE37435C/en",
        "source_type": "government",
        "language": "de",
    },
    "henry-ford-model-n": {
        "title": "1906 Ford Model N Runabout",
        "publisher": "The Henry Ford",
        "url": "https://thehenryford.org/collections-and-research/digital-collections/artifact/50201",
        "source_type": "museum",
        "language": "en",
    },
}

RECORDS = {
    "Benz Patent Motor Car Model 1": {
        "description": (
            "Primeira unidade do Patent-Motorwagen, o veículo que a Benz & Co. de Mannheim "
            "registrou no Deutsches Reichspatent 37435, depositado em 29 de janeiro de 1886. O "
            "texto da patente descreve uma construção destinada sobretudo a carros leves e "
            "pequenas embarcações para o transporte de uma a quatro pessoas. O arquivo da "
            "Mercedes-Benz atribui o projeto a Carl Benz."
        ),
        "dates": {"designed_by": {"from": "1886", "precision": "year"}},
        "confront": [{
            "predicate": "designed_by",
            "source": "dpma-patent-37435",
            "locator": {"patent": "DE 37435 C", "filed": "1886-01-29", "published": "1886-11-02",
                        "section": "Beschreibung, parágrafo de abertura"},
            "excerpt": PATENT_QUOTE,
            "evidence_type": "patent_record",
            "note": (
                "Registro governamental: o depósito de 29 de janeiro de 1886 fixa a data por ato de "
                "terceiro, sem depender do arquivo da Mercedes-Benz. O requerente consta como Benz "
                "& Co., de Mannheim; a atribuição pessoal a Carl Benz permanece sustentada apenas "
                "pelo fabricante."
            ),
        }],
    },
    "Ford Model N": {
        "description": (
            "Automóvel de dois lugares fabricado pela Ford a partir de 1906, antecessor direto do "
            "Model T. O museu The Henry Ford conserva um exemplar sob o número de inventário "
            "85.115.1, datado de 1906, e registra que, a 500 dólares, o Model N tornou-se o "
            "automóvel mais vendido dos Estados Unidos."
        ),
        "dates": {"manufactured_by": {"from": "1906", "precision": "year"}},
        "confront": [{
            "predicate": "manufactured_by",
            "source": "henry-ford-model-n",
            "locator": {"inventory_number": "85.115.1", "section": "Overview", "object_date": "1906"},
            "excerpt": MODEL_N_QUOTE,
            "evidence_type": "collection_record",
            "note": (
                "Confronto independente: a ficha de acervo data o objeto de 1906 e é do museu, não "
                "da Ford Motor Company."
            ),
        }],
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
    matches = [r for r in rows if r["predicate"] == plan["predicate"]]
    if fragment := plan.get("object_like"):
        matches = [r for r in matches if fragment.lower() in str(r["object_text"] or r["object_name"] or "").lower()]
    if len(matches) != 1:
        raise ValueError(f"alvo ambíguo ou ausente para {plan['predicate']}: {len(matches)} statements")
    return matches[0]["statement_id"]


def resolve_source(db, key):
    meta = SOURCES[key]
    existing = db.execute("SELECT id FROM source WHERE url=?", (meta["url"],)).fetchone()
    if existing:
        return existing["id"], False
    source_id = stable_uuid7(f"source:{meta['url']}")
    db.execute(
        """INSERT INTO source
           (id,source_type,title,author,publisher,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at)
           VALUES (?,?,?,?,?,?,?,?,'primary','{}',?,?,?)""",
        (source_id, meta["source_type"], meta["title"], meta.get("author"), meta["publisher"],
         meta["url"], NOW, meta.get("language"),
         f"Fonte independente introduzida na passagem {BATCH}.", NOW, NOW),
    )
    return source_id, True


def confront(db, name, statement_id, plan):
    source_id, minted = resolve_source(db, plan["source"])
    seed = f"{name}:{plan['predicate']}:{SOURCES[plan['source']]['url']}"
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
    return minted


def main():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    dated = confronted = minted = reused = 0
    try:
        for name, record in RECORDS.items():
            entity_id, metadata_json = entity_row(db, name)
            rows = statement_rows(db, entity_id)

            for predicate, window in record["dates"].items():
                target = pick_statement(rows, {"predicate": predicate})
                db.execute(
                    """UPDATE statement SET valid_from=?, valid_from_precision=?,
                       valid_until=?, valid_until_precision=?, updated_at=? WHERE id=?""",
                    (window["from"], window["precision"], window.get("until"),
                     window["precision"] if window.get("until") else None, NOW, target),
                )
                dated += 1

            for plan in record.get("confront", []):
                if confront(db, name, pick_statement(rows, plan), plan):
                    minted += 1
                else:
                    reused += 1
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
        "independentClaimsAdded": confronted, "sourcesMinted": minted, "sourcesReused": reused,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
