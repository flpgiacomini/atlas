#!/usr/bin/env python3
"""Complete CP19 C06/M01: review the 23 remaining pioneer brands."""

from __future__ import annotations

import json
import re
import sqlite3
import unicodedata
from pathlib import Path

from enrich_people_batch_01 import stable_uuid7

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
NOW = "2026-08-25T23:30:00+00:00"

# name: title, publisher, url, decision, year, milestone, description
RECORDS = {
    "Austin": ("Longbridge factory", "British Motor Museum", "https://www.britishmotormuseum.co.uk/explore/museum-blog/factor-us-in-longbridge-factory", "promote-editorial", 1905, "Austin estabelece sua fábrica em Longbridge", "Fabricante britânica fundada por Herbert Austin em 1905. Longbridge e o Austin Seven fizeram da marca uma referência na motorização britânica de grande escala."),
    "Clément-Bayard": ("Adolphe Clément", "Museo Nazionale dell'Automobile", "https://www.museoauto.com/en/qrcode/adolphe-clement/", "promote-editorial", 1903, "Clément-Bayard consolida sua identidade automotiva", "Marca francesa de Adolphe Clément, importante na passagem das bicicletas e triciclos para automóveis, motores e produção industrial no início do século XX."),
    "Darracq": ("Darracq 12 CV Open Tourer", "Museu do Caramulo", "https://museudocaramulo.pt/en/colecoes/darracq-12-cv-open-tourer-2/", "promote-editorial", 1897, "Darracq ingressa na fabricação de automóveis", "Fabricante francesa associada à produção em série, à competição e à expansão industrial internacional que alimentou linhagens posteriores na Europa."),
    "Hispano-Suiza": ("Our history", "Hispano Suiza Cars", "https://www.hispanosuizacars.com/our-history/", "promote-editorial", 1904, "Hispano-Suiza é fundada em Barcelona", "Marca hispano-suíça fundada em Barcelona em 1904, reconhecida pela engenharia de Marc Birkigt, por automóveis de luxo e pela transferência de conhecimentos entre automóveis e aviação."),
    "Humber": ("Conserving a car: Humber 16/50 Tourer", "Coventry Transport Museum", "https://transport-museum.com/news/1490/conserving-a-car-humber-1650-tourer", "promote-editorial", 1897, "Humber produz seu primeiro automóvel", "Marca britânica originada na indústria de ciclos, fabricante de automóveis desde 1897 e depois parte do grupo Rootes, representativa da consolidação industrial de Coventry."),
    "Isotta Fraschini": ("Storia della Isotta Fraschini", "Museo Nazionale dell'Automobile", "https://www.museoauto.com/fr/qrcode/storia-della-isotta-fraschini/", "promote-editorial", 1900, "Isotta Fraschini é fundada em Milão", "Fabricante italiana fundada em 1900, ligada a automóveis de prestígio, soluções técnicas avançadas e à projeção internacional da engenharia e do luxo italianos."),
    "Itala": ("Storia della Itala", "Museo Nazionale dell'Automobile", "https://www.museoauto.com/fr/qrcode/storia-della-itala/", "promote-editorial", 1904, "Itala nasce em Turim", "Marca italiana fundada em 1904, historicamente relevante por sua engenharia e pela vitória na prova Pequim–Paris de 1907, demonstração extrema de resistência e alcance do automóvel."),
    "Laurin & Klement": ("125 years ago Laurin and Klement laid the foundation stone for ŠKODA AUTO", "Škoda Auto", "https://cdn.skoda-storyboard.com/2020/12/201221-125-years-ago-Vaclav-Laurin-and-Vaclav-Klement-laid-the-foundation-stone-for-SKODA-AUTO.pdf", "promote-editorial", 1895, "Laurin & Klement inicia a linhagem da Škoda", "Empresa fundada em 1895 por Václav Laurin e Václav Klement: começou com bicicletas, passou a motocicletas e automóveis e foi integrada à Škoda em 1925."),
    "Locomobile": ("Locomobile steam car", "Smithsonian National Museum of American History", "https://americanhistory.si.edu/collections/object/nmah_840131", "promote-editorial", 1899, "Locomobile inicia a produção de carros a vapor", "Fabricante norte-americana que produziu automóveis a vapor a partir de 1899 e depois adotou motores a gasolina, documentando a competição entre sistemas de propulsão no mercado inicial."),
    "Maxwell": ("Chrysler Corporation", "Detroit Historical Society", "https://www.detroithistorical.org/learn/online-research/encyclopedia-of-detroit/chrysler-corporation", "promote-editorial", 1904, "Maxwell entra no mercado norte-americano", "Fabricante norte-americana de grande volume cuja estrutura empresarial e industrial deu origem à Chrysler Corporation em 1925."),
    "Mors": ("Mors, 1902", "Science Museum Group", "https://collection.sciencemuseumgroup.org.uk/objects/co478031/mors-1902", "promote-editorial", 1902, "Mors leva a velocidade ao centro da narrativa automotiva", "Fabricante francesa pioneira em competição. O Mors preservado pelo Science Museum Group está ligado aos recordes de velocidade de 1902 e ao desenvolvimento do automóvel de alto desempenho."),
    "Napier": ("D. Napier & Son Ltd", "Science Museum Group", "https://collection.sciencemuseumgroup.org.uk/people/ap26897/d-napier-and-son-ltd", "promote-editorial", 1900, "Napier produz um automóvel de seis cilindros", "Empresa britânica de engenharia que fabricou um pioneiro automóvel de seis cilindros em 1900 e conectou automóveis, competição e motores aeronáuticos."),
    "Opel": ("21 January 1899: Opel starts the automobile age", "Stellantis / Opel", "https://www.media.stellantis.com/de-de/opel/press/21-januar-1899-vor-125-jahren-startet-opel-ins-automobilzeitalter", "promote-editorial", 1899, "Opel inicia oficialmente a produção de automóveis", "Empresa alemã fundada em 1862 que ingressou na fabricação de automóveis em 1899, conectando máquinas de costura, bicicletas e produção automotiva de grande escala."),
    "Packard": ("Packard Motor Car Company", "Detroit Historical Society", "https://www.detroithistorical.org/learn/online-research/encyclopedia-of-detroit/packard-motor-car-company", "promote-editorial", 1899, "O primeiro Packard é construído", "Fabricante norte-americana fundada no ciclo de 1899, referência em luxo e engenharia e mais tarde unida à Studebaker; sua trajetória termina em 1958."),
    "Peerless": ("Cleveland automotive history", "Western Reserve Historical Society", "https://www.wrhs.org/files/assets/westsidedrivingtourofautomotivehistory.pdf", "retain-catalog", 1900, "Peerless integra o polo automotivo de Cleveland", "Marca de luxo do polo industrial de Cleveland. Permanece no catálogo: a fonte regional confirma o contexto, mas o C06 não encontrou documentação institucional específica suficiente para promoção editorial autônoma."),
    "Pierce-Arrow": ("Pierce-Arrow 125th Anniversary", "Pierce-Arrow Museum", "https://www.pierce-arrow.com/events/pierce-arrow-125th-anniversary/", "promote-editorial", 1901, "Pierce produz seu primeiro automóvel", "Fabricante norte-americana de Buffalo, reconhecida por automóveis de luxo, qualidade construtiva e soluções de identidade visual que marcaram o segmento de prestígio."),
    "Rambler": ("Thomas B. Jeffery Company", "Wisconsin Historical Society", "https://www.wisconsinhistory.org/Records/Article/CS344", "promote-editorial", 1902, "Rambler estabelece uma linhagem industrial em Wisconsin", "Marca produzida pela Thomas B. Jeffery Company, elo fundador de uma linhagem que passa por Nash e American Motors e chega à consolidação posterior com a Chrysler."),
    "REO": ("R. E. Olds Transportation Museum", "R. E. Olds Transportation Museum", "https://www.reoldsmuseum.org/", "retain-catalog", 1904, "REO surge no polo industrial de Lansing", "Marca fundada por R. E. Olds em Lansing. Permanece no catálogo até que uma fonte institucional específica sustente, em detalhe, sua contribuição e cronologia automotivas."),
    "Rochet-Schneider": ("Rochet-Schneider", "Musée de l'Automobile Henri Malartre", "https://www.musee-malartre.com/en/node/375", "promote-editorial", 1894, "Rochet-Schneider inicia sua trajetória em Lyon", "Fabricante de Lyon fundada por Édouard Rochet e Théodore Schneider, relevante por exportações, licenciamento e pelo desenvolvimento do polo automotivo francês."),
    "Studebaker": ("The Studebaker history", "Studebaker National Museum", "https://studebakermuseum.org/archives-and-education/the-studebaker-history/", "promote-editorial", 1902, "Studebaker passa das carruagens ao automóvel elétrico", "Empresa norte-americana fundada em 1852 na era das carruagens, produtora de automóveis elétricos desde 1902 e participante de uma das mais longas transições industriais da mobilidade."),
    "Tatra": ("TATRA TRUCKS company profile", "Tatra Trucks", "https://www.tatra.cz/data/files/TATRA-TRUCKS-company-profile-web-CZ-1.pdf", "promote-editorial", 1919, "O nome Tatra passa a identificar a linhagem da Nesselsdorfer", "Linhagem da fabricante de Kopřivnice, uma das mais antigas do mundo automotivo. O nome Tatra, adotado em 1919, conecta automóveis pioneiros e uma tradição técnica de longa duração."),
    "Vauxhall": ("Vauxhall celebrates 60 years of vehicle production at Ellesmere Port", "Stellantis / Vauxhall", "https://www.media.stellantis.com/uk-en/vauxhall/press/vauxhall-celebrates-60-years-of-vehicle-production-at-ellesmere-port", "promote-editorial", 1903, "Vauxhall inicia a produção de automóveis", "Fabricante britânica de veículos desde 1903, transferida para Luton em 1905 e importante na industrialização automotiva do Reino Unido."),
    "Wolseley": ("Wolseley 6hp", "British Motor Museum", "https://www.britishmotormuseum.co.uk/online-collections/details-page?row_id=76417800473", "promote-editorial", 1901, "Wolseley inicia a produção comercial de automóveis", "Marca britânica cuja fase automotiva foi desenhada por Herbert Austin; seus primeiros modelos documentam a formação da indústria britânica no início do século XX."),
}


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def main() -> None:
    db = sqlite3.connect(DB)
    try:
        for name, (title, publisher, url, decision, _year, _milestone, description) in RECORDS.items():
            row = db.execute("SELECT id, metadata_json FROM entity WHERE canonical_name=? AND entity_type='brand'", (name,)).fetchone()
            if not row:
                raise ValueError(f"brand candidate not found: {name}")
            existing = db.execute("SELECT id FROM source WHERE url=? ORDER BY id LIMIT 1", (url,)).fetchone()
            source_id = existing[0] if existing else stable_uuid7("source:" + url)
            db.execute("""INSERT INTO source(id,source_type,title,publisher,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at)
                VALUES(?,'institutional',?,?,?,'2026-08-25','en','A','{}','Fonte da revisão CP19 C06/M01B.',?,?)
                ON CONFLICT(id) DO UPDATE SET title=excluded.title,publisher=excluded.publisher,accessed_at=excluded.accessed_at,updated_at=excluded.updated_at""",
                (source_id, title, publisher, url, NOW, NOW))
            metadata = json.loads(row[1] or "{}")
            metadata.update({
                "curation_batch": "C06-M01B", "curation_review": f"atlas:curation-review:c06-{slugify(name)}",
                "curation_reviewed_at": "2026-08-25", "curation_decision": decision,
                "curation_source_ids": [source_id], "editorial_level": "catalog",
                "promotion_state": "approved_pending_v2_cut" if decision == "promote-editorial" else "retained_catalog_after_review",
                "verification_state": "source_backed", "verified_at": "2026-08-25",
            })
            db.execute("UPDATE entity SET description=?, metadata_json=?, updated_at=? WHERE id=?",
                       (description, json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, row[0]))
        db.commit()
    except Exception:
        db.rollback(); raise
    finally:
        db.close()
    promote = sum(r[3] == "promote-editorial" for r in RECORDS.values())
    print(json.dumps({"batch": "C06-M01B", "reviewed": len(RECORDS), "promote": promote, "retain": len(RECORDS)-promote}))


if __name__ == "__main__":
    main()
