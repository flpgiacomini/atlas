#!/usr/bin/env python3
"""Publish Lincoln Futura, Cadillac Cyclone and Chevrolet Corvair Monza GT."""
import json
import sqlite3
from pathlib import Path

from enrich_people_batch_01 import stable_uuid7

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
NOW = "2026-08-19T16:30:00+00:00"

SOURCES = {
    "Futura": (
        "manufacturer_archive",
        "Lincoln en los comics: el primer Batimóvil",
        "Lincoln / Ford Motor Company",
        "2022-08-03",
        "https://media.ford.com/content/lincolnmedia/lna/mx/es/news/2022/08/03/lincoln-en-los-comics--el-primer-batimovil.html",
        "es",
    ),
    "Futura paint": (
        "manufacturer_archive",
        "Ford comemora 80 anos do seu estúdio de design",
        "Ford Motor Company",
        "2015-07-23",
        "https://media.ford.com/content/fordmedia/fsa/br/pt/news/2015/07/23/ford-comemora-80-anos-de-inovacao-do--seu-estudio-de-design.html",
        "pt-BR",
    ),
    "Cyclone": (
        "manufacturer_archive",
        "Iconic Then, Iconic Now: Our Legacy",
        "Cadillac / General Motors",
        None,
        "https://www.cadillac.com/collectors-showcase/heritage",
        "en",
    ),
    "Cyclone radar": (
        "museum_collection",
        "1959 Cadillac Cyclone XP-74",
        "Taubman Museum of Art",
        "2018-11-21",
        "https://www.taubmanmuseum.org/page/2/?search=Irving",
        "en",
    ),
    "Monza GT": (
        "manufacturer_archive",
        "1962 Chevrolet Corvair Monza GT Concept",
        "General Motors Heritage Collection",
        None,
        "https://www.gm.com/heritage/collection/chevrolet/1962-chevrolet-corvair-monza-gt",
        "en",
    ),
}

ENTITIES = {
    "Lincoln Futura": ("vehicle", "Concept car funcional de 1955 concebido pelos designers da Ford John Najjar e William M. Schmid, com carroceria artesanal produzida pela Ghia em Turim. Além de experimentar pintura perolizada, o exemplar atravessou cinema e televisão: George Barris o transformou no Batmóvel da série de 1966, tornando-o uma ponte rara entre pesquisa de estilo e cultura popular.", {"vehicle_level": "standalone", "vehicle_kind": "concept", "editorial_batch": "V05"}),
    "Cadillac Cyclone": ("vehicle", "Concept car de 1959 que encerrou a linhagem dos Motoramas sob forte inspiração aeroespacial. Seus cones dianteiros alojavam sensores de radar para advertência de proximidade, enquanto a capota transparente retrátil e as portas deslizantes dramatizavam um futuro automatizado; o projeto permaneceu experimental e integra a coleção histórica da General Motors.", {"vehicle_level": "standalone", "vehicle_kind": "concept", "editorial_batch": "V05"}),
    "Chevrolet Corvair Monza GT": ("vehicle", "Concept car experimental de 1962 cujas linhas aerodinâmicas resultaram de ensaios em túnel de vento. A arquitetura reunia motor boxer de seis cilindros refrigerado a ar, seção traseira basculante para acesso mecânico, cabine com assentos reclinados e canopy envolvente aberto para a frente, documentando a pesquisa esportiva da Chevrolet no início dos anos 1960.", {"vehicle_level": "standalone", "vehicle_kind": "concept", "editorial_batch": "V05"}),
    "Lincoln": ("brand", "Marca norte-americana de automóveis de luxo da Ford Motor Company. Sua história conecta veículos de produção e estudos de estilo; o Futura de 1955 ocupa posição singular por reunir fabricação transatlântica, experimentação de materiais e posterior circulação como ícone da cultura audiovisual.", {"brand_status": "active", "editorial_batch": "V05"}),
    "Chevrolet": ("brand", "Marca da General Motors ligada à produção de automóveis de passageiros, esportivos e programas experimentais. No Atlas, o Corvair Monza GT representa sua pesquisa de aerodinâmica, ergonomia e arquitetura mecânica aplicada a concepts no início da década de 1960.", {"brand_status": "active", "editorial_batch": "V05"}),
    "John Najjar": ("person", "Designer da Ford Motor Company creditado pela Lincoln, ao lado de William M. Schmid, pela concepção do Futura de 1955. O projeto combinou referências aeronáuticas e uma carroceria construída pela Ghia antes de adquirir uma segunda vida como veículo de cinema e televisão.", {"roles": ["automotive designer"], "editorial_batch": "V05"}),
    "William M. Schmid": ("person", "Designer da Ford Motor Company creditado pela Lincoln, ao lado de John Najjar, pela concepção do Futura de 1955. Sua participação integra o estudo ao ambiente profissional de design da Ford, antes da construção artesanal da carroceria na Itália.", {"roles": ["automotive designer"], "editorial_batch": "V05"}),
    "Ghia": ("organization", "Carrozzeria e casa de design de Turim responsável por produzir artesanalmente a carroceria do Lincoln Futura. A colaboração exemplifica a circulação transatlântica de conhecimento entre estúdios de fabricantes norte-americanos e oficinas italianas de protótipos.", {"organization_type": "coachbuilder and design house", "editorial_batch": "V05"}),
    "Pintura automotiva perolizada": ("technology", "Acabamento que incorpora partículas de efeito para produzir brilho e variação visual na pintura. A Ford registra o Futura de 1955 como um marco inicial de apresentação pública da técnica, então obtida com pérolas trituradas adicionadas ao revestimento.", {"technology_category": "materials and finish", "editorial_batch": "V05"}),
    "Alerta automotivo de colisão por radar": ("technology", "Sistema experimental de assistência que usa radar para detectar obstáculos adiante e advertir o motorista. No Cadillac Cyclone, sensores instalados nos cones dianteiros produziam alertas de proximidade, antecipando uma linha de pesquisa posteriormente difundida em sistemas de segurança veicular.", {"technology_category": "active safety", "editorial_batch": "V05"}),
    "Canopy retrátil automotivo": ("technology", "Solução experimental que substitui ou complementa teto e portas convencionais por uma cobertura transparente móvel. No Cadillac Cyclone, a bolha retrátil reforçava tanto a visibilidade panorâmica quanto a linguagem aeroespacial do concept car.", {"technology_category": "body and access", "editorial_batch": "V05"}),
    "Desenvolvimento aerodinâmico em túnel de vento": ("technology", "Método de pesquisa no qual modelos ou veículos são expostos a fluxo de ar controlado para observar e reduzir arrasto, sustentação e turbulência. A General Motors atribui diretamente as linhas do Corvair Monza GT a um programa de testes em túnel de vento.", {"technology_category": "aerodynamics", "editorial_batch": "V05"}),
    "Motor boxer refrigerado a ar": ("technology", "Arquitetura de motor com cilindros horizontalmente opostos e refrigeração por fluxo de ar, dispensando circuito líquido. O Corvair Monza GT empregou um seis-cilindros desse tipo, acessível pela seção traseira basculante da carroceria.", {"technology_category": "propulsion architecture", "editorial_batch": "V05"}),
    "Canopy automotivo com abertura dianteira": ("technology", "Configuração de acesso em que a cobertura envolvente da cabine bascula para a frente. No Corvair Monza GT, a solução liberava o compartimento dos passageiros e integrava acesso, visibilidade e forma aerodinâmica em um único elemento.", {"technology_category": "body and access", "editorial_batch": "V05"}),
}

RELATIONS = {
    "Lincoln Futura": [("designed_by", "John Najjar", "Futura"), ("designed_by", "William M. Schmid", "Futura"), ("manufactured_by", "Ghia", "Futura"), ("marketed_under", "Lincoln", "Futura"), ("uses_technology", "Pintura automotiva perolizada", "Futura paint")],
    "Cadillac Cyclone": [("marketed_under", "Cadillac", "Cyclone"), ("uses_technology", "Linguagem aeronáutica em concept cars", "Cyclone"), ("uses_technology", "Alerta automotivo de colisão por radar", "Cyclone radar"), ("uses_technology", "Canopy retrátil automotivo", "Cyclone radar")],
    "Chevrolet Corvair Monza GT": [("marketed_under", "Chevrolet", "Monza GT"), ("uses_technology", "Desenvolvimento aerodinâmico em túnel de vento", "Monza GT"), ("uses_technology", "Motor boxer refrigerado a ar", "Monza GT"), ("uses_technology", "Canopy automotivo com abertura dianteira", "Monza GT")],
}


def entity_id(db, name):
    row = db.execute("SELECT id FROM entity WHERE canonical_name=?", (name,)).fetchone()
    if not row:
        raise ValueError(name)
    return row[0]


def main():
    db = sqlite3.connect(DB)
    db.execute("PRAGMA foreign_keys=ON")
    try:
        for name, (kind, description, metadata) in ENTITIES.items():
            db.execute("""INSERT INTO entity(id,entity_type,canonical_name,slug,description,metadata_json,created_at,updated_at)
                VALUES(?,?,?,NULL,?,?,?,?) ON CONFLICT(id) DO UPDATE SET description=excluded.description,
                metadata_json=excluded.metadata_json,updated_at=excluded.updated_at""",
                (stable_uuid7("entity:" + name), kind, name, description, json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, NOW))

        source_ids = {}
        for key, (kind, title, publisher, published_at, url, language) in SOURCES.items():
            source_ids[key] = stable_uuid7("source:" + url)
            db.execute("""INSERT OR IGNORE INTO source(id,source_type,title,publisher,published_at,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at)
                VALUES(?,?,?,?,?,?,'2026-08-19',?,'A','{}','Registro institucional ou museológico do veículo e de suas soluções.',?,?)""",
                (source_ids[key], kind, title, publisher, published_at, url, language, NOW, NOW))

        # V05 originally inferred a GM Design credit not stated by the linked record.
        # Remove that deterministic assertion before publishing the source-explicit relation.
        legacy_seed = "Cadillac Cyclone:developed_by:GM Design:V05"
        legacy_claim = stable_uuid7("claim:" + legacy_seed)
        legacy_evidence = stable_uuid7("evidence:" + legacy_seed)
        legacy_statement = stable_uuid7("statement:" + legacy_seed)
        db.execute("DELETE FROM claim_evidence WHERE claim_id=?", (legacy_claim,))
        db.execute("DELETE FROM claim WHERE id=?", (legacy_claim,))
        db.execute("DELETE FROM statement WHERE id=?", (legacy_statement,))
        db.execute("DELETE FROM evidence WHERE id=?", (legacy_evidence,))

        for subject, relations in RELATIONS.items():
            statement_ids = []
            for predicate, obj, source_key in relations:
                seed = f"{subject}:{predicate}:{obj}:V05"
                statement_id = stable_uuid7("statement:" + seed)
                statement_ids.append(statement_id)
                predicate_id = db.execute("SELECT id FROM predicate WHERE name=?", (predicate,)).fetchone()[0]
                db.execute("""INSERT OR IGNORE INTO statement(id,subject_entity_id,predicate_id,object_type,object_entity_id,qualifiers_json,confidence,resolution_status,created_at,updated_at)
                    VALUES(?,?,?,'entity',?,?,'high','accepted',?,?)""",
                    (statement_id, entity_id(db, subject), predicate_id, entity_id(db, obj), json.dumps({"editorial_batch": "V05", "source_record": source_key}, ensure_ascii=False), NOW, NOW))
                claim_id = stable_uuid7("claim:" + seed)
                evidence_id = stable_uuid7("evidence:" + seed)
                db.execute("INSERT OR IGNORE INTO claim(id,statement_id,stance,support_strength,note,created_at) VALUES(?,?,'supports','explicit','Relação documentada pela fonte vinculada.',?)", (claim_id, statement_id, NOW))
                db.execute("INSERT OR IGNORE INTO evidence(id,source_id,evidence_type,locator_json,notes,created_at) VALUES(?,?,'collection_record',?,'Fonte institucional ou museológica consultada para o lote V05.',?)", (evidence_id, source_ids[source_key], json.dumps({"vehicle": subject, "predicate": predicate}, ensure_ascii=False), NOW))
                db.execute("INSERT OR IGNORE INTO claim_evidence(claim_id,evidence_id) VALUES(?,?)", (claim_id, evidence_id))
            metadata = ENTITIES[subject][2] | {"description_basis_statement_ids": statement_ids}
            db.execute("UPDATE entity SET metadata_json=? WHERE canonical_name=?", (json.dumps(metadata, ensure_ascii=False, sort_keys=True), subject))
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    print(json.dumps({"published": list(RELATIONS), "support_entities": 11, "relations": sum(map(len, RELATIONS.values()))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
