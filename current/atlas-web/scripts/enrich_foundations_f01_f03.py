#!/usr/bin/env python3
"""Import the selected pre-1886 foundations with evidence and explicit uncertainty."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
NOW = "2026-08-18T22:30:00+00:00"


def uuid7(seed: str) -> str:
    raw = bytearray(hashlib.sha256(f"atlas-foundations-f01-f03:{seed}".encode()).digest()[:16])
    raw[6] = (raw[6] & 0x0F) | 0x70
    raw[8] = (raw[8] & 0x3F) | 0x80
    value = raw.hex()
    return f"{value[:8]}-{value[8:12]}-{value[12:16]}-{value[16:20]}-{value[20:]}"


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


SOURCES = {
    "cugnot": ("Fardier à vapeur de Joseph Cugnot", "Musée des Arts et Métiers", "https://www.arts-et-metiers.net/musee/fardier-vapeur-de-joseph-cugnot", "fr", "A"),
    "trevithick": ("Richard Trevithick", "Science Museum Group Collection", "https://collection.sciencemuseumgroup.org.uk/people/ap269/trevithick-richard", "en", "A"),
    "rivaz": ("Le moteur à combustion — François Isaac de Rivaz", "Institut national de la propriété industrielle", "https://artsandculture.google.com/asset/le-moteur-%C3%A0-combustion-fran%C3%A7ois-isaac-de-rivaz-brevet-d-invention-d%C3%A9pos%C3%A9-le-16-05-1805-pour-des-machines-dont-le-principe-moteur-est-l-explosion-des-gaz-et-autres-substances-a%C3%A9riformes-1ba544/VQFCB5DXRKDDmg?hl=fr", "fr", "A"),
    "early_engine": ("History of the automobile", "Encyclopaedia Britannica", "https://www.britannica.com/technology/automobile/History-of-the-automobile", "en", "B"),
    "bollee": ("L'Obéissante, voiture à vapeur d'Amédée Bollée", "Musée des 24 Heures du Mans", "https://www.lemans-musee24h.com/", "fr", "B"),
    "marcus": ("The second Marcus car", "Technisches Museum Wien", "https://www.technischesmuseum.at/", "de", "B"),
    "benz": ("Benz patent motor car (Model 1)", "Mercedes-Benz Public Archive", "https://mercedes-benz-publicarchive.com/marsClassic/en/instance/ko/Benz-patent-motor-car-Model-1.xhtml?oid=4376", "en", "A"),
}


ENTITIES = {
    "Nicolas-Joseph Cugnot": ("person", "Engenheiro militar francês associado ao fardier a vapor construído entre 1769 e 1771. Seu trabalho documenta uma experiência inicial de veículo rodoviário autopropelido, concebida para uma finalidade militar e anterior em mais de um século ao automóvel leve a gasolina.", {"roles": ["engineer", "inventor"], "editorial_batch": "F01"}),
    "Fardier à vapeur de Cugnot": ("vehicle", "Veículo rodoviário autopropelido a vapor desenvolvido por Nicolas-Joseph Cugnot para transportar material de artilharia. O exemplar preservado permite tratar o projeto como precursor documentado, sem convertê-lo anacronicamente em equivalente direto do automóvel de passageiros moderno.", {"vehicle_level": "model", "vehicle_kind": "experimental", "editorial_batch": "F01"}),
    "Richard Trevithick": ("person", "Engenheiro britânico que desenvolveu motores compactos de vapor de alta pressão e os aplicou a veículos rodoviários entre 1801 e 1803. Seus ensaios demonstraram a possibilidade de maior relação entre potência e massa, embora sem continuidade comercial estável.", {"roles": ["engineer", "inventor"], "editorial_batch": "F01"}),
    "Puffing Devil": ("vehicle", "Veículo rodoviário experimental a vapor construído por Richard Trevithick em 1801, em Camborne. É um marco da aplicação do vapor de alta pressão à mobilidade terrestre, conhecido por documentação histórica e reconstruções que precisam permanecer diferenciadas do artefato original.", {"vehicle_level": "model", "vehicle_kind": "experimental", "editorial_batch": "F01"}),
    "London Steam Carriage": ("vehicle", "Carruagem rodoviária a vapor apresentada por Richard Trevithick em Londres em 1803. O veículo levou a experimentação de alta pressão a um ambiente urbano e ilustra simultaneamente a capacidade técnica alcançada e as limitações econômicas e operacionais do período.", {"vehicle_level": "model", "vehicle_kind": "experimental", "editorial_batch": "F01"}),
    "François Isaac de Rivaz": ("person", "Inventor e político franco-suíço que patenteou uma máquina baseada na explosão de gases e realizou experiências de propulsão veicular. Seu caso constitui uma fundação da combustão interna, mas patente, motor e veículo devem conservar datas e níveis de evidência separados.", {"roles": ["inventor", "engineer"], "editorial_batch": "F01"}),
    "Veículo experimental de Rivaz": ("vehicle", "Veículo experimental atribuído a François Isaac de Rivaz e movido por um motor de combustão interna com mistura gasosa. O registro no Atlas distingue a patente de 1805 das experiências veiculares posteriores e evita uma reivindicação simplificada de prioridade absoluta.", {"vehicle_level": "model", "vehicle_kind": "experimental", "editorial_batch": "F01"}),
    "Propulsão rodoviária a vapor": ("technology", "Aplicação de motores a vapor a veículos que se deslocam por vias públicas, em contraste com usos estacionários e ferroviários. A tecnologia formou uma trajetória própria, condicionada por massa, água, pressão, infraestrutura, operação e regulação durante o século XIX.", {"technology_category": "propulsion", "editorial_batch": "F01"}),
    "Motor de combustão interna": ("technology", "Tecnologia que converte em trabalho mecânico a energia liberada pela combustão dentro do motor. Antes do automóvel a gasolina, experiências com diferentes gases, ignição e arquiteturas estabeleceram princípios que seriam refinados ao longo do século XIX.", {"technology_category": "propulsion", "editorial_batch": "F01"}),
    "Étienne Lenoir": ("person", "Inventor franco-belga cujo motor comercial a gás e as experiências veiculares do início da década de 1860 ajudaram a demonstrar a combustão interna fora do laboratório. Sua contribuição precedeu os motores eficientes de quatro tempos e revelou limitações importantes.", {"roles": ["inventor", "engineer"], "editorial_batch": "F02"}),
    "Hippomobile de Lenoir": ("vehicle", "Veículo experimental associado a Étienne Lenoir e usualmente datado de 1863, impulsionado por uma adaptação de seu motor. Ele representa uma etapa entre o motor comercial estacionário e a propulsão rodoviária por combustão interna.", {"vehicle_level": "model", "vehicle_kind": "experimental", "editorial_batch": "F02"}),
    "Alphonse Beau de Rochas": ("person", "Engenheiro francês que formulou e patenteou em 1862 princípios do ciclo de quatro tempos. O Atlas separa essa formulação documental da posterior realização prática e comercial, evitando atribuir todo o desenvolvimento do motor moderno a um único inventor.", {"roles": ["engineer", "inventor"], "editorial_batch": "F02"}),
    "Nikolaus August Otto": ("person", "Engenheiro alemão ligado à realização prática e comercial do motor de quatro tempos na década de 1870. Sua contribuição é registrada em relação com a formulação anterior de Beau de Rochas e com as disputas técnicas e jurídicas subsequentes.", {"roles": ["engineer", "inventor", "entrepreneur"], "editorial_batch": "F02"}),
    "Ciclo de quatro tempos": ("technology", "Ciclo termodinâmico de admissão, compressão, combustão e escape que se tornou central para o motor automotivo. Sua história reúne formulação, patente, construção e comercialização por agentes distintos, exigindo atribuições específicas para cada etapa.", {"technology_category": "propulsion", "editorial_batch": "F02"}),
    "Amédée Bollée": ("person", "Fundidor, inventor e construtor francês responsável por veículos rodoviários a vapor de grande porte. Com L’Obéissante, demonstrou em 1875 que uma máquina autopropelida podia transportar passageiros em uma viagem pública entre cidades.", {"roles": ["inventor", "manufacturer"], "editorial_batch": "F02"}),
    "L’Obéissante": ("vehicle", "Veículo rodoviário a vapor construído por Amédée Bollée em 1873 e conduzido de Le Mans a Paris em 1875. Sua escala e capacidade de passageiros oferecem um contraponto à narrativa centrada exclusivamente nos pequenos veículos a gasolina.", {"vehicle_level": "model", "vehicle_kind": "experimental", "editorial_batch": "F02"}),
    "Viagem de L’Obéissante a Paris": ("event", "Viagem pública realizada em 1875 por Amédée Bollée com L’Obéissante entre Le Mans e Paris. O episódio demonstrou alcance rodoviário para passageiros, ao mesmo tempo que expôs dificuldades regulatórias e operacionais enfrentadas pelos veículos a vapor.", {"event_type": "demonstration", "realization_status": "occurred", "editorial_batch": "F02"}),
    "Dugald Clerk": ("person", "Engenheiro escocês associado ao desenvolvimento de um motor funcional de dois tempos no final da década de 1870. Sua presença amplia o Atlas para além da genealogia do ciclo Otto e mostra alternativas técnicas contemporâneas.", {"roles": ["engineer", "inventor"], "editorial_batch": "F03"}),
    "Ciclo de dois tempos": ("technology", "Ciclo de motor que completa sua sequência operacional em duas movimentações do pistão. Desenvolvido em formas práticas no século XIX, constituiu uma alternativa tecnológica relevante, ainda que suas aplicações automotivas posteriores tenham seguido trajetória própria.", {"technology_category": "propulsion", "editorial_batch": "F03"}),
    "Siegfried Marcus": ("person", "Inventor germano-austríaco associado a veículos experimentais com motor de combustão interna. As datas e a prioridade tradicionalmente atribuídas a seus automóveis são discutidas, por isso o Atlas conserva a controvérsia como parte do registro, não como conclusão.", {"roles": ["inventor", "engineer"], "editorial_batch": "F03"}),
    "Segundo automóvel de Marcus": ("vehicle", "Veículo preservado atribuído a Siegfried Marcus e frequentemente inserido nas disputas sobre os primeiros automóveis a gasolina. Sua datação histórica permanece controversa, exigindo qualificadores e fontes independentes antes de qualquer afirmação de prioridade.", {"vehicle_level": "model", "vehicle_kind": "experimental", "editorial_batch": "F03"}),
    "Édouard Delamare-Deboutteville": ("person", "Industrial e inventor francês ligado, com Léon Malandin, a uma patente e a experiências de veículo movido a combustível líquido em 1884. O caso será tratado como reivindicação documentada, sem converter prioridade nacional em consenso mundial.", {"roles": ["inventor", "industrialist"], "editorial_batch": "F03"}),
    "Léon Malandin": ("person", "Mecânico francês que colaborou com Édouard Delamare-Deboutteville no desenvolvimento de motores e de um veículo experimental em 1884. O Atlas o registra como participante técnico, preservando a autoria compartilhada indicada pela patente.", {"roles": ["mechanic", "inventor"], "editorial_batch": "F03"}),
    "Veículo Delamare-Deboutteville–Malandin": ("vehicle", "Veículo experimental francês associado à patente de Delamare-Deboutteville e Malandin em 1884. Integra a discussão sobre a convergência do motor a combustível líquido e da carruagem, mas sua prioridade depende da definição e da documentação utilizada.", {"vehicle_level": "model", "vehicle_kind": "experimental", "editorial_batch": "F03"}),
    "Ensaios do Benz Patent-Motorwagen em 1885": ("event", "Fase de construção e ensaios do Benz Patent-Motorwagen durante 1885, anterior ao depósito de patente de janeiro de 1886. O evento cria a ponte cronológica entre a experimentação pré-1886 e a série anual principal do Atlas.", {"event_type": "vehicle_test", "realization_status": "occurred", "editorial_batch": "F03"}),
}


# subject, predicate, object kind, object, date precision, confidence, resolution, source
STATEMENTS = [
    ("Fardier à vapeur de Cugnot", "developed_by", "entity", "Nicolas-Joseph Cugnot", None, "high", "accepted", "cugnot"),
    ("Fardier à vapeur de Cugnot", "uses_technology", "entity", "Propulsão rodoviária a vapor", None, "high", "accepted", "cugnot"),
    ("Fardier à vapeur de Cugnot", "occurred_on", "date", "1769", "year", "high", "accepted", "cugnot"),
    ("Fardier à vapeur de Cugnot", "configured_as", "string", "trator de artilharia experimental", None, "high", "accepted", "cugnot"),
    ("Nicolas-Joseph Cugnot", "born_on", "date", "1725", "year", "high", "accepted", "cugnot"),
    ("Nicolas-Joseph Cugnot", "died_on", "date", "1804", "year", "high", "accepted", "cugnot"),
    ("Puffing Devil", "developed_by", "entity", "Richard Trevithick", None, "high", "accepted", "trevithick"),
    ("Puffing Devil", "uses_technology", "entity", "Propulsão rodoviária a vapor", None, "high", "accepted", "trevithick"),
    ("Puffing Devil", "occurred_on", "date", "1801", "year", "high", "accepted", "trevithick"),
    ("Puffing Devil", "configured_as", "string", "veículo rodoviário experimental", None, "high", "accepted", "trevithick"),
    ("London Steam Carriage", "developed_by", "entity", "Richard Trevithick", None, "high", "accepted", "trevithick"),
    ("London Steam Carriage", "uses_technology", "entity", "Propulsão rodoviária a vapor", None, "high", "accepted", "trevithick"),
    ("London Steam Carriage", "occurred_on", "date", "1803", "year", "high", "accepted", "trevithick"),
    ("London Steam Carriage", "configured_as", "string", "carruagem rodoviária de passageiros", None, "high", "accepted", "trevithick"),
    ("Richard Trevithick", "born_on", "date", "1771", "year", "high", "accepted", "trevithick"),
    ("Richard Trevithick", "died_on", "date", "1833", "year", "high", "accepted", "trevithick"),
    ("Veículo experimental de Rivaz", "developed_by", "entity", "François Isaac de Rivaz", None, "medium", "accepted", "rivaz"),
    ("Veículo experimental de Rivaz", "uses_technology", "entity", "Motor de combustão interna", None, "high", "accepted", "rivaz"),
    ("Veículo experimental de Rivaz", "occurred_on", "date", "1807", "year", "medium", "needs_reconciliation", "rivaz"),
    ("Veículo experimental de Rivaz", "configured_as", "string", "carro experimental movido por mistura gasosa", None, "medium", "needs_reconciliation", "rivaz"),
    ("François Isaac de Rivaz", "born_on", "date", "1752", "year", "high", "accepted", "rivaz"),
    ("François Isaac de Rivaz", "died_on", "date", "1828", "year", "high", "accepted", "rivaz"),
    ("Hippomobile de Lenoir", "developed_by", "entity", "Étienne Lenoir", None, "medium", "accepted", "early_engine"),
    ("Hippomobile de Lenoir", "uses_technology", "entity", "Motor de combustão interna", None, "high", "accepted", "early_engine"),
    ("Hippomobile de Lenoir", "occurred_on", "date", "1863", "year", "medium", "accepted", "early_engine"),
    ("Hippomobile de Lenoir", "configured_as", "string", "veículo rodoviário experimental", None, "medium", "accepted", "early_engine"),
    ("Étienne Lenoir", "born_on", "date", "1822", "year", "high", "accepted", "early_engine"),
    ("Étienne Lenoir", "died_on", "date", "1900", "year", "high", "accepted", "early_engine"),
    ("Ciclo de quatro tempos", "invented_by", "entity", "Alphonse Beau de Rochas", None, "medium", "accepted", "early_engine"),
    ("Ciclo de quatro tempos", "developed_by", "entity", "Nikolaus August Otto", None, "high", "accepted", "early_engine"),
    ("Ciclo de quatro tempos", "occurred_on", "date", "1862", "year", "high", "accepted", "early_engine"),
    ("Alphonse Beau de Rochas", "born_on", "date", "1815", "year", "high", "accepted", "early_engine"),
    ("Alphonse Beau de Rochas", "died_on", "date", "1893", "year", "high", "accepted", "early_engine"),
    ("Nikolaus August Otto", "born_on", "date", "1832", "year", "high", "accepted", "early_engine"),
    ("Nikolaus August Otto", "died_on", "date", "1891", "year", "high", "accepted", "early_engine"),
    ("L’Obéissante", "developed_by", "entity", "Amédée Bollée", None, "high", "accepted", "bollee"),
    ("L’Obéissante", "uses_technology", "entity", "Propulsão rodoviária a vapor", None, "high", "accepted", "bollee"),
    ("L’Obéissante", "occurred_on", "date", "1873", "year", "medium", "accepted", "bollee"),
    ("Viagem de L’Obéissante a Paris", "involved", "entity", "L’Obéissante", None, "high", "accepted", "bollee"),
    ("Viagem de L’Obéissante a Paris", "involved", "entity", "Amédée Bollée", None, "high", "accepted", "bollee"),
    ("Viagem de L’Obéissante a Paris", "occurred_on", "date", "1875", "year", "high", "accepted", "bollee"),
    ("Amédée Bollée", "born_on", "date", "1844", "year", "high", "accepted", "bollee"),
    ("Ciclo de dois tempos", "developed_by", "entity", "Dugald Clerk", None, "high", "accepted", "early_engine"),
    ("Ciclo de dois tempos", "based_on", "entity", "Motor de combustão interna", None, "high", "accepted", "early_engine"),
    ("Ciclo de dois tempos", "occurred_on", "date", "1878", "year", "medium", "accepted", "early_engine"),
    ("Dugald Clerk", "born_on", "date", "1854", "year", "high", "accepted", "early_engine"),
    ("Dugald Clerk", "died_on", "date", "1932", "year", "high", "accepted", "early_engine"),
    ("Segundo automóvel de Marcus", "developed_by", "entity", "Siegfried Marcus", None, "high", "accepted", "marcus"),
    ("Segundo automóvel de Marcus", "uses_technology", "entity", "Motor de combustão interna", None, "high", "accepted", "marcus"),
    ("Segundo automóvel de Marcus", "occurred_on", "date", "1888", "year", "disputed", "needs_reconciliation", "marcus"),
    ("Siegfried Marcus", "born_on", "date", "1831", "year", "high", "accepted", "marcus"),
    ("Siegfried Marcus", "died_on", "date", "1898", "year", "high", "accepted", "marcus"),
    ("Veículo Delamare-Deboutteville–Malandin", "developed_by", "entity", "Édouard Delamare-Deboutteville", None, "medium", "accepted", "early_engine"),
    ("Veículo Delamare-Deboutteville–Malandin", "developed_by", "entity", "Léon Malandin", None, "medium", "accepted", "early_engine"),
    ("Veículo Delamare-Deboutteville–Malandin", "uses_technology", "entity", "Motor de combustão interna", None, "medium", "accepted", "early_engine"),
    ("Veículo Delamare-Deboutteville–Malandin", "occurred_on", "date", "1884", "year", "medium", "needs_reconciliation", "early_engine"),
    ("Édouard Delamare-Deboutteville", "collaborated_with", "entity", "Léon Malandin", None, "high", "accepted", "early_engine"),
    ("Édouard Delamare-Deboutteville", "born_on", "date", "1856", "year", "high", "accepted", "early_engine"),
    ("Léon Malandin", "collaborated_with", "entity", "Édouard Delamare-Deboutteville", None, "high", "accepted", "early_engine"),
    ("Ensaios do Benz Patent-Motorwagen em 1885", "involved", "entity", "Benz Patent Motor Car", None, "high", "accepted", "benz"),
    ("Ensaios do Benz Patent-Motorwagen em 1885", "involved", "entity", "Carl Benz", None, "high", "accepted", "benz"),
    ("Ensaios do Benz Patent-Motorwagen em 1885", "occurred_on", "date", "1885", "year", "high", "accepted", "benz"),
    ("Benz Patent Motor Car", "uses_technology", "entity", "Ciclo de quatro tempos", None, "high", "accepted", "benz"),
    ("Gottlieb Daimler", "collaborated_with", "entity", "Wilhelm Maybach", None, "high", "accepted", "benz"),
]


def entity_id(db: sqlite3.Connection, name: str) -> str:
    row = db.execute("SELECT id FROM entity WHERE canonical_name=?", (name,)).fetchone()
    if not row:
        raise ValueError(f"Missing entity: {name}")
    return row[0]


def main() -> None:
    db = sqlite3.connect(DB)
    db.execute("PRAGMA foreign_keys=ON")
    try:
        for name, (kind, description, metadata) in ENTITIES.items():
            db.execute(
                """INSERT INTO entity (id,entity_type,canonical_name,slug,description,metadata_json,created_at,updated_at)
                   VALUES (?,?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET description=excluded.description,
                   metadata_json=excluded.metadata_json,updated_at=excluded.updated_at""",
                (uuid7(f"entity:{name}"), kind, name, slugify(name), description,
                 json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, NOW),
            )
        source_ids = {}
        for key, (title, publisher, url, language, tier) in SOURCES.items():
            source_id = uuid7(f"source:{url}")
            source_ids[key] = source_id
            db.execute(
                """INSERT OR IGNORE INTO source
                   (id,source_type,title,publisher,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at)
                   VALUES (?,'institutional',?,?,?,?,?,?,'{}',?,?,?)""",
                (source_id, title, publisher, url, "2026-08-18", language, tier,
                 "Fonte-semente do lote F01-F03; afirmações controversas permanecem qualificadas.", NOW, NOW),
            )
        for subject, predicate, object_kind, obj, precision, confidence, resolution, source_key in STATEMENTS:
            predicate_row = db.execute("SELECT id FROM predicate WHERE name=?", (predicate,)).fetchone()
            if not predicate_row:
                raise ValueError(f"Missing predicate: {predicate}")
            seed = f"{subject}:{predicate}:{object_kind}:{obj}"
            statement_id = uuid7(f"statement:{seed}")
            object_entity_id = entity_id(db, obj) if object_kind == "entity" else None
            object_date = obj if object_kind == "date" else None
            object_text = obj if object_kind == "string" else None
            qualifiers = {"editorial_batch": "F01-F03"}
            if resolution in {"needs_reconciliation", "rejected"}:
                qualifiers["priority_claim_policy"] = "Não interpretar como prioridade absoluta; preservar divergência historiográfica."
            db.execute(
                """INSERT OR IGNORE INTO statement
                   (id,subject_entity_id,predicate_id,object_type,object_entity_id,object_text,object_date,object_date_precision,
                    qualifiers_json,confidence,resolution_status,created_at,updated_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (statement_id, entity_id(db, subject), predicate_row[0], object_kind, object_entity_id, object_text,
                 object_date, precision, json.dumps(qualifiers, ensure_ascii=False), confidence, resolution, NOW, NOW),
            )
            claim_id = uuid7(f"claim:{seed}")
            evidence_id = uuid7(f"evidence:{seed}")
            stance = "contradicts" if resolution == "rejected" else "qualifies" if resolution == "needs_reconciliation" else "supports"
            strength = "weak" if confidence in {"low", "disputed"} else "strong" if confidence == "medium" else "explicit"
            db.execute(
                "INSERT OR IGNORE INTO claim (id,statement_id,stance,support_strength,note,created_at) VALUES (?,?,?,?,?,?)",
                (claim_id, statement_id, stance, strength,
                 "Registro do lote F01-F03; datas, função do veículo e reivindicações de prioridade são mantidas separadas.", NOW),
            )
            db.execute(
                """INSERT OR IGNORE INTO evidence (id,source_id,evidence_type,locator_json,notes,created_at)
                   VALUES (?,?,'web_page',?,?,?)""",
                (evidence_id, source_ids[source_key], json.dumps({"subject": subject, "predicate": predicate}, ensure_ascii=False),
                 "Fonte consultada como ponto de partida editorial; sem reprodução de texto protegido.", NOW),
            )
            db.execute("INSERT OR IGNORE INTO claim_evidence (claim_id,evidence_id) VALUES (?,?)", (claim_id, evidence_id))
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    print(json.dumps({"entities": len(ENTITIES), "statements": len(STATEMENTS), "status": "ok"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
