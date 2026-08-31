#!/usr/bin/env python3
"""Documentary pass D08: two GM concepts and a Peugeot quadricycle.

Reached by changing which sources the batch goes after rather than which route
it takes to them. Several institutions refuse the fetcher outright, so this pass
targets vehicles covered by the museums already proven reachable — the Audrain's
General Motors exhibit and the Musée des Arts et Métiers — instead of retrying
doors that stay shut.

The Peugeot Type 3 is the sharpest case. Its museum record was already in the
source registry, catalogued and unused: the entity cited only Stellantis. The
record was never linked, so the batch attaches the source that already existed
rather than introducing a new one.

The Le Sabre is the weakest and is labelled as such. The Audrain dates it in the
exhibit heading and nowhere in the body, so the evidence is recorded as an
exhibit label with the heading as its excerpt, and the note says outright that no
sentence in the page states the year. That is a real confrontation — the museum
is not General Motors — but it is a weaker one than a stated sentence, and the
record should not pretend otherwise.

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
BATCH = "D08"
NOW = "2026-08-31T23:00:00+00:00"

FIREBIRD_QUOTE = (
    "Built in 1958, it was the only member of the Firebird trio to have any direct impact on the "
    "design of General Motors production vehicles."
)
LESABRE_HEADING = "1951 Le Sabre Concept"
PEUGEOT_QUOTE = "Armand Peugeot can se lancer dans la production de véhicules à essence"


def stable_uuid7(seed: str) -> str:
    raw = bytearray(hashlib.sha256(f"atlas-documentary-d08:{seed}".encode()).digest()[:16])
    raw[6] = (raw[6] & 0x0F) | 0x70
    raw[8] = (raw[8] & 0x3F) | 0x80
    h = raw.hex()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


SOURCES = {
    "audrain-le-sabre": {
        "title": "1951 Le Sabre Concept",
        "publisher": "Audrain Auto Museum",
        "url": "https://www.audrainautomuseum.org/styling-the-future/1951-le-sabre-concept",
        "source_type": "museum",
        "language": "en",
    },
    "audrain-firebird-iii": {
        "title": "1958 Firebird III",
        "publisher": "Audrain Auto Museum",
        "url": "https://www.audrainautomuseum.org/styling-the-future/1958-firebird-iii",
        "source_type": "museum",
        "language": "en",
    },
    "arts-et-metiers-peugeot-type-3": {
        "title": "Quadricycle Peugeot Type 3",
        "publisher": "Musée des Arts et Métiers",
        "url": "https://www.arts-et-metiers.net/musee/quadricycle-peugeot-type-3",
        "source_type": "museum",
        "language": "fr",
    },
}

RECORDS = {
    "General Motors Le Sabre": {
        "description": (
            "Concept car construído sob a liderança de Harley Earl para levar ao automóvel a "
            "linguagem da propulsão a jato então difundida na aviação. O Audrain Auto Museum, que o "
            "expõe como “1951 Le Sabre Concept”, descreve quatro macacos hidráulicos sob o carro "
            "para troca de pneu e serviço simples — recurso que, segundo o museu, a Fórmula 1 "
            "adotaria anos depois —, além de sensor automático de chuva para a capota, bancos "
            "aquecidos, faróis ocultos e carburação dupla a metanol."
        ),
        "dates": {"developed_by": {"from": "1951", "precision": "year"}},
        "confront": [{
            "predicate": "developed_by",
            "source": "audrain-le-sabre",
            "locator": {"exhibit": "Styling the Future", "heading": LESABRE_HEADING},
            "excerpt": LESABRE_HEADING,
            "evidence_type": "exhibit_label",
            "note": (
                "Confronto independente da data, em grau fraco: o museu data o objeto no título da "
                "exposição e nenhuma frase do corpo da página afirma o ano. Vale como fonte fora da "
                "General Motors, não como afirmação textual."
            ),
        }],
    },
    "General Motors Firebird III": {
        "description": (
            "Terceiro concept car da linhagem Firebird, construído em 1958. O Audrain Auto Museum o "
            "identifica como o único dos três Firebird a influenciar diretamente o desenho dos "
            "automóveis de produção da General Motors, e aponta que o Cadillac de 1959 herdou parte "
            "de seu tratamento de superfície e o de 1961, as quilhas traseiras."
        ),
        "dates": {"developed_by": {"from": "1958", "precision": "year"}},
        "confront": [{
            "predicate": "developed_by",
            "source": "audrain-firebird-iii",
            "locator": {"exhibit": "Styling the Future", "quote": "Built in 1958"},
            "excerpt": FIREBIRD_QUOTE,
            "evidence_type": "explicit_statement",
            "note": (
                "Confronto independente da data: o museu afirma em texto que o Firebird III foi "
                "construído em 1958, fora do arquivo da General Motors."
            ),
        }],
    },
    "Peugeot Type 3": {
        "description": (
            "Quadriciclo fabricado em 1892 e conservado pelo Musée des Arts et Métiers sob o número "
            "de inventário 16593. A ficha do museu situa o Type 3 na entrada da Peugeot na produção "
            "de veículos a gasolina, viabilizada pela parceria com a Panhard et Levassor, detentora "
            "dos direitos exclusivos de fabricação na França do motor a petróleo Daimler."
        ),
        "dates": {"marketed_under": {"from": "1892", "precision": "year"}},
        "confront": [{
            "predicate": "marketed_under",
            "source": "arts-et-metiers-peugeot-type-3",
            "locator": {"inventory_number": "16593", "section": "Notice de l'objet", "field": "Date de fabrication"},
            "excerpt": PEUGEOT_QUOTE,
            "evidence_type": "collection_record",
            "note": (
                "Confronto independente: a ficha do museu data a fabricação de 1892 sob o "
                "inventário 16593. Esta fonte já constava no registro do Atlas sem estar ligada a "
                "esta entidade, que citava apenas a Stellantis."
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
    """Reuse a registered source before minting one.

    The corpus already carries sources that no claim cites — the Peugeot's museum
    record among them — so keying on the URL keeps one row per document instead
    of a second row describing the same page.
    """
    meta = SOURCES[key]
    existing = db.execute("SELECT id FROM source WHERE url=?", (meta["url"],)).fetchone()
    if existing:
        return existing["id"], False
    source_id = stable_uuid7(f"source:{meta['url']}")
    db.execute(
        """INSERT INTO source
           (id,source_type,title,author,publisher,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at)
           VALUES (?,?,?,?,?,?,?,?,'specialist','{}',?,?,?)""",
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
