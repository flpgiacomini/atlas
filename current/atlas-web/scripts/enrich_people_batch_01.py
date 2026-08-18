#!/usr/bin/env python3
"""Idempotent, evidence-backed enrichment for the first biographical batch."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "atlas.sqlite"
REGISTRY_PATH = ROOT.parent / "canonical-model" / "PREDICATE_REGISTRY_v1.0.json"
NOW = "2026-08-18T18:00:00+00:00"


def stable_uuid7(seed: str) -> str:
    raw = bytearray(hashlib.sha256(f"atlas-editorial-01:{seed}".encode()).digest()[:16])
    raw[6] = (raw[6] & 0x0F) | 0x70
    raw[8] = (raw[8] & 0x3F) | 0x80
    h = raw.hex()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


PEOPLE = {
    "Carl Benz": {
        "description": "Engenheiro e empreendedor alemão que desenvolveu o automóvel movido a gasolina patenteado em 1886. Sua trajetória uniu pesquisa mecânica, fabricação de motores e liderança empresarial, estabelecendo uma das bases técnicas e industriais da mobilidade moderna.",
        "source": {
            "title": "Carl Benz: inventor and entrepreneur",
            "publisher": "Mercedes-Benz Group",
            "url": "https://group.mercedes-benz.com/company/tradition/founders-pioneers/carl-benz.html",
            "language": "en",
        },
        "statements": [
            ("born_on", "date", "1844-11-25", "day", None, None),
            ("died_on", "date", "1929-04-04", "day", None, None),
            ("worked_at", "entity", "Benz & Cie.", None, "1883", "year"),
            ("led", "entity", "Benz & Cie.", None, "1883", "year"),
        ],
    },
    "Henry Ford": {
        "description": "Engenheiro e industrial norte-americano que construiu o Quadricycle em 1896 e fundou a Ford Motor Company em 1903. Tornou-se figura decisiva na transformação do automóvel em produto de grande escala e no desenvolvimento da indústria moderna.",
        "source": {
            "title": "Henry Ford Biography",
            "publisher": "The Henry Ford",
            "url": "https://www.thehenryford.org/collections/explore/videos/henry-ford",
            "language": "en",
        },
        "statements": [
            ("born_on", "date", "1863-07-30", "day", None, None),
            ("died_on", "date", "1947-04-07", "day", None, None),
            ("worked_at", "entity", "Ford Motor Company", None, "1903-06-16", "day"),
            ("led", "entity", "Ford Motor Company", None, "1903-06-16", "day"),
        ],
    },
    "Richard Attwood": {
        "description": "Piloto britânico com passagem pela Fórmula 1 e pelos protótipos de longa duração. Como piloto oficial da Porsche, venceu as 24 Horas de Le Mans de 1970 ao lado de Hans Herrmann, obtendo a primeira vitória geral da marca na prova.",
        "source": {
            "title": "Porsche congratulates Richard Attwood on his 85th birthday",
            "publisher": "Porsche Newsroom",
            "published_at": "2025-04-04",
            "url": "https://newsroom.porsche.com/en_US/2025/motorsport/porsche-congratulates-richard-attwood-85-years-39110.html",
            "language": "en",
        },
        "statements": [
            ("born_on", "date", "1940-04-04", "day", None, None),
            ("worked_at", "entity", "Dr. Ing. h.c. F. Porsche AG", None, "1969", "year"),
            ("collaborated_with", "entity", "Hans Herrmann", None, "1970-06-14", "day"),
        ],
    },
    "Nils Bohlin": {
        "description": "Engenheiro sueco especializado em segurança que desenvolveu o cinto de três pontos em formato de V para a Volvo. A solução, introduzida em 1959 e liberada para uso amplo, tornou-se uma referência mundial de proteção automotiva.",
        "source": {
            "title": "Volvo Cars Heritage",
            "publisher": "Volvo Cars",
            "url": "https://www.volvocars.com/en-ca/our-heritage/",
            "language": "en",
        },
        "statements": [
            ("born_on", "date", "1920", "year", None, None),
            ("worked_at", "entity", "Volvo Cars", None, "1958", "year"),
        ],
    },
    "Ferdinand Alexander Porsche": {
        "description": "Designer alemão responsável pela forma original do Porsche 911 e por projetos como o 904 Carrera GTS. Ingressou na empresa familiar em 1957, assumiu a direção de design em 1961 e depois fundou o Porsche Design Studio.",
        "source": {
            "title": "90 years of Ferdinand Alexander Porsche",
            "publisher": "Porsche Newsroom",
            "published_at": "2025-12-11",
            "url": "https://newsroom.porsche.com/en_PAP/2025/history/porsche-ferdinand-alexander-90-years-41290.html",
            "language": "en",
        },
        "statements": [
            ("born_on", "date", "1935-12-11", "day", None, None),
            ("worked_at", "entity", "Dr. Ing. h.c. F. Porsche AG", None, "1957", "year"),
            ("led", "entity", "Dr. Ing. h.c. F. Porsche AG", None, "1961", "year"),
        ],
    },
}


def entity_id(db: sqlite3.Connection, name: str) -> str:
    row = db.execute("SELECT id FROM entity WHERE canonical_name=?", (name,)).fetchone()
    if not row:
        raise ValueError(f"Missing entity: {name}")
    return row[0]


def upsert_predicates(db: sqlite3.Connection) -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    for item in registry:
        if item["name"] not in {"born_on", "died_on"}:
            continue
        db.execute(
            """INSERT OR IGNORE INTO predicate
               (id,name,description,subject_types_json,object_types_json,temporal_policy,symmetric,status,created_at)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (item["id"], item["name"], item["description"], json.dumps(item["subject_types"]),
             json.dumps(item["object_types"]), item["temporal_policy"], int(item["symmetric"]), item["status"], NOW),
        )


def add_statement(db: sqlite3.Connection, person: str, source_id: str, spec: tuple) -> None:
    predicate, object_type, value, precision, valid_from, valid_precision = spec
    subject_id = entity_id(db, person)
    predicate_id = db.execute("SELECT id FROM predicate WHERE name=?", (predicate,)).fetchone()[0]
    seed = f"statement:{person}:{predicate}:{value}"
    statement_id = stable_uuid7(seed)
    object_entity = entity_id(db, value) if object_type == "entity" else None
    object_date = value if object_type == "date" else None
    db.execute(
        """INSERT OR IGNORE INTO statement
           (id,subject_entity_id,predicate_id,object_type,object_entity_id,object_date,object_date_precision,
            valid_from,valid_from_precision,qualifiers_json,confidence,resolution_status,created_at,updated_at)
           VALUES (?,?,?,?,?,?,?,?,?,'{}','high','accepted',?,?)""",
        (statement_id, subject_id, predicate_id, object_type, object_entity, object_date, precision,
         valid_from, valid_precision, NOW, NOW),
    )
    claim_id = stable_uuid7(f"claim:{seed}")
    evidence_id = stable_uuid7(f"evidence:{seed}")
    db.execute(
        "INSERT OR IGNORE INTO claim (id,statement_id,stance,support_strength,note,created_at) VALUES (?,?,'supports','explicit',?,?)",
        (claim_id, statement_id, "Afirmação biográfica documentada pela fonte institucional indicada.", NOW),
    )
    db.execute(
        """INSERT OR IGNORE INTO evidence
           (id,source_id,evidence_type,locator_json,excerpt,notes,created_at)
           VALUES (?,?,'web_page',?,NULL,?,?)""",
        (evidence_id, source_id, json.dumps({"section": person}, ensure_ascii=False),
         f"Verificação editorial do predicado {predicate}; sem reprodução de trecho protegido.", NOW),
    )
    db.execute("INSERT OR IGNORE INTO claim_evidence (claim_id,evidence_id) VALUES (?,?)", (claim_id, evidence_id))


def main() -> None:
    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA foreign_keys=ON")
    try:
        upsert_predicates(db)
        for person, item in PEOPLE.items():
            db.execute(
                "UPDATE entity SET description=?, updated_at=? WHERE canonical_name=?",
                (item["description"], NOW, person),
            )
            source = item["source"]
            source_id = stable_uuid7(f"source:{source['url']}")
            db.execute(
                """INSERT OR IGNORE INTO source
                   (id,source_type,title,author,publisher,published_at,url,accessed_at,language,source_tier,
                    zotero_key,external_ids_json,notes,created_at,updated_at)
                   VALUES (?,'institutional',?,NULL,?,?,?,?,?,'A',NULL,'{}',?, ?, ?)""",
                (source_id, source["title"], source["publisher"], source.get("published_at"), source["url"],
                 "2026-08-18", source["language"], "Fonte institucional verificada para o lote editorial 01.", NOW, NOW),
            )
            for statement in item["statements"]:
                add_statement(db, person, source_id, statement)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    print(json.dumps({"people_enriched": len(PEOPLE), "status": "ok"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
