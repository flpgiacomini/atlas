#!/usr/bin/env python3
"""Add source-backed narratives and brand relations to priority catalog records."""
import json
import sqlite3
from pathlib import Path

from enrich_people_batch_01 import stable_uuid7

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
NOW = "2026-08-20T13:00:00+00:00"

RECORDS = {
    "Chrysler Turbine Car": {"brand": "Chrysler", "description": "Programa experimental apresentado pela Chrysler em 1963 para avaliar a turbina a gás no uso cotidiano. Cinquenta automóveis foram cedidos a famílias para testes, com carrocerias Ghia produzidas em Turim. A experiência demonstrou suavidade e flexibilidade de combustível, mas também expôs consumo elevado, emissões e atraso de resposta que limitaram a produção em série.", "source": ("museum_collection", "1964 Chrysler Turbine Car", "Smithsonian National Museum of American History", None, "https://americanhistory.si.edu/collections/object/nmah_687503", "en", "A")},
    "Mercedes-Benz C 111": {"brand": "Mercedes-Benz", "description": "Laboratório rodante apresentado pela Mercedes-Benz na IAA de Frankfurt de 1969. A carroceria em plástico reforçado com fibra de vidro, as portas asa-de-gaivota e o motor Wankel de três rotores reuniam pesquisa de materiais, aerodinâmica e propulsão. O programa não chegou à produção, mas originou versões posteriores usadas em ensaios diesel e recordes de velocidade.", "source": ("manufacturer_archive", "50 Jahre Markenlegende C 111", "Mercedes-Benz Classic", "2019-04-09", "https://media.mercedes-benz.com/article/945bbb64-f554-4fa3-8d9d-6b8f417610b4", "de", "A")},
    "Aston Martin Bulldog": {"brand": "Aston Martin", "description": "Protótipo rodoviário de motor central construído entre 1978 e 1980 para explorar a ambição de um Aston Martin capaz de superar 200 mph. O projeto de portas asa-de-gaivota alcançou 191 mph nos testes de época, mas foi cancelado por custos. Restaurado décadas depois, comprovou a promessa original ao registrar 205,4 mph em 2023.", "source": ("heritage_archive", "Bulldog 200", "Aston Martin Heritage Trust", "2023-06-29", "https://amht.org.uk/bulldog-200/", "en", "A")},
    "Volkswagen W12": {"brand": "Volkswagen", "description": "Estudo superesportivo iniciado em 1997 para demonstrar a arquitetura compacta W12 desenvolvida pela Volkswagen. O motor combinava duas bancadas derivadas do VR6, permitindo doze cilindros em um conjunto curto. A evolução W12 Nardò, com chassi de fibra de carbono e motor central, foi usada em recordes de longa duração e antecipou a aplicação do W12 em automóveis de luxo do grupo.", "source": ("manufacturer_publication", "Mission Maximum: Records and superlatives from the world of Volkswagen", "Volkswagen Classic", "2018-06-30", "https://www.volkswagen-newsroom.com/en/publications/more/mission-maximum-180/download", "en", "A")},
    "Maybach Exelero": {"brand": "Maybach", "description": "Concept coupé criado em 2005 como demonstrador para o pneu de alto desempenho Fulda Carat Exelero, retomando uma parceria histórica entre Fulda e Maybach. Com mais de 700 cv, o exemplar funcionou como plataforma técnica e peça de comunicação; em 1º de maio de 2005 atingiu 351,45 km/h em uma prova de alta velocidade.", "source": ("corporate_archive", "Fulda history", "Fulda", None, "https://www.fulda.com/en_gb/consumer/about-us/history.html", "en", "A")},
    "Ferrari P4/5 by Pininfarina": {"brand": "Ferrari", "description": "One-off apresentado em 2006, desenvolvido pela Pininfarina para James Glickenhaus a partir de uma Ferrari Enzo. O projeto reinterpretou proporções e referências dos protótipos esportivos Ferrari da série P em uma carroceria inteiramente nova. Sua relevância está no encontro entre plataforma contemporânea, encomenda individual e tradição italiana de carrozzeria.", "source": ("technical_publication", "Passion for Speed: Ferrari P4/5 by Pininfarina", "Paolo Garella", None, "https://www.paologarella.com/img_press/file/1374001168_Brochure_P45_Dimomedia_web.pdf", "en", "B")},
}


def entity_id(db, name):
    row = db.execute("SELECT id FROM entity WHERE canonical_name=?", (name,)).fetchone()
    if not row:
        raise ValueError(f"Entidade ausente: {name}")
    return row[0]


def main():
    db = sqlite3.connect(DB)
    db.execute("PRAGMA foreign_keys=ON")
    predicate_id = db.execute("SELECT id FROM predicate WHERE name='marketed_under'").fetchone()[0]
    try:
        for name, record in RECORDS.items():
            vehicle_id = entity_id(db, name)
            brand_id = entity_id(db, record["brand"])
            kind, title, publisher, published_at, url, language, tier = record["source"]
            source_id = stable_uuid7("source:" + url)
            db.execute("""INSERT INTO source(id,source_type,title,publisher,published_at,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at)
                VALUES(?,?,?,?,?,?,'2026-08-20',?,?,'{}','Fonte individual usada na verificação catalográfica R01.',?,?)
                ON CONFLICT(id) DO UPDATE SET title=excluded.title,publisher=excluded.publisher,published_at=excluded.published_at,accessed_at=excluded.accessed_at,updated_at=excluded.updated_at""",
                (source_id, kind, title, publisher, published_at, url, language, tier, NOW, NOW))
            seed = f"{name}:marketed_under:{record['brand']}:R01"
            statement_id = stable_uuid7("statement:" + seed)
            claim_id = stable_uuid7("claim:" + seed)
            evidence_id = stable_uuid7("evidence:" + seed)
            db.execute("""INSERT INTO statement(id,subject_entity_id,predicate_id,object_type,object_entity_id,qualifiers_json,confidence,resolution_status,created_at,updated_at)
                VALUES(?,?,?,'entity',?,?,'high','accepted',?,?) ON CONFLICT(id) DO UPDATE SET object_entity_id=excluded.object_entity_id,qualifiers_json=excluded.qualifiers_json,updated_at=excluded.updated_at""",
                (statement_id, vehicle_id, predicate_id, brand_id, json.dumps({"editorial_batch": "R01", "verification_scope": "brand_attribution"}, sort_keys=True), NOW, NOW))
            db.execute("INSERT OR IGNORE INTO claim(id,statement_id,stance,support_strength,note,created_at) VALUES(?,?,'supports','explicit','Atribuição documentada pela fonte individual R01.',?)", (claim_id, statement_id, NOW))
            db.execute("INSERT OR IGNORE INTO evidence(id,source_id,evidence_type,locator_json,notes,created_at) VALUES(?,?,'web_record',?,'Fonte consultada para identidade, contexto e atribuição de marca.',?)", (evidence_id, source_id, json.dumps({"entity": name, "accessed_at": "2026-08-20"}, ensure_ascii=False), NOW))
            db.execute("INSERT OR IGNORE INTO claim_evidence(claim_id,evidence_id) VALUES(?,?)", (claim_id, evidence_id))
            metadata = json.loads(db.execute("SELECT metadata_json FROM entity WHERE id=?", (vehicle_id,)).fetchone()[0] or "{}")
            metadata.update({"verification_state": "source_backed", "verified_at": "2026-08-20", "verification_batch": "R01", "promotion_state": "waiting_media_and_second_source", "description_basis_statement_ids": [statement_id]})
            db.execute("UPDATE entity SET description=?,metadata_json=?,updated_at=? WHERE id=?", (record["description"], json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, vehicle_id))
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    print(json.dumps({"batch": "R01", "source_backed": len(RECORDS), "relations": len(RECORDS)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
