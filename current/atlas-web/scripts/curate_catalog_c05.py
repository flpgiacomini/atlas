#!/usr/bin/env python3
"""Apply CP19 C05 sources and reviewed decisions to the transition database."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from enrich_people_batch_01 import stable_uuid7

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
NOW = "2026-08-25T21:00:00+00:00"

RECORDS = {
    "BMW E1": ("promote-editorial", "80 years of BMW car production: the origins of EfficientDynamics", "BMW Group", "https://www.press.bmwgroup.com/global/article/detail/T0022917EN/80-years-of-bmw-car-production-the-origins-of-efficientdynamics", "Automóvel elétrico experimental apresentado em 1991 que combinou propulsão sem emissões locais, baixo peso e materiais recicláveis como programa integrado de eficiência."),
    "Mercedes-Benz F 100": ("promote-editorial", "1991: F 100 research vehicle", "Mercedes-Benz Public Archive", "https://mercedes-benz-archive.com/marsClassic/en/instance/ko/1991.xhtml?oid=4912515", "Veículo de pesquisa apresentado em Detroit em 1991 que reorganizou o habitáculo em torno da segurança e reuniu sistemas eletrônicos posteriormente associados à produção Mercedes-Benz."),
    "Renault Scénic Concept": ("promote-editorial", "Renault and family cars: 50 years of history since the Renault 16", "Renault Group", "https://www.renaultgroup.com/en/magazine/our-group-news/renault-and-the-familiy-cars-50-years-of-history-since-the-renault-16/", "Conceito familiar apresentado em 1991 cuja organização espacial e denominação foram levadas ao Scénic de produção em 1996, marco do monovolume compacto europeu."),
    "Chrysler Atlantic": ("retain-catalog", "Chrysler heritage", "Stellantis North America", "https://www.stellantisnorthamerica.com/heritage/", "Show car de 1995 preservado no catálogo. A revisão não encontrou no acervo institucional consultado uma ficha individual que demonstre transferência tecnológica ou derivação de produção."),
    "Ford GT90": ("retain-catalog", "Ford Heritage Vault", "Ford Motor Company", "https://www.fordheritagevault.com/", "Superesportivo conceitual de 1995 mantido no catálogo. A notoriedade e a experimentação formal não substituem uma fonte institucional individual que comprove consequência histórica posterior."),
    "Toyota Prius Concept": ("promote-editorial", "Prius Concept – evolution", "Toyota Motor Corporation", "https://global.toyota/en/prius20th/evolution/concept/", "Conceito híbrido apresentado em 1995 como precursor direto do Prius lançado em 1997, documentando a passagem de um programa experimental à produção em série."),
    "Audi AL2": ("promote-editorial", "Leading light: the Audi A2 launched 25 years ago", "Audi MediaCenter", "https://www.audi-mediacenter.com/en/press-releases/leading-light-the-audi-a2-launched-25-years-ago-16857/download", "Estudo de alumínio apresentado em 1997 que antecipou o Audi A2 de produção e estendeu a construção leve Audi Space Frame a um automóvel compacto de grande volume interno."),
    "Volkswagen 1-Litre Car": ("promote-editorial", "The XL1 – the car", "Volkswagen Newsroom", "https://www.volkswagen-newsroom.com/en/the-xl1-3163/the-xl1-the-car-3178", "Protótipo de 2002 construído para demonstrar consumo de um litro por 100 quilômetros. A Volkswagen documenta sua continuidade no L1 de 2009 e no XL1 de pequena série."),
    "BMW GINA Light Visionary Model": ("promote-editorial", "The BMW GINA Light Visionary Model", "BMW Group", "https://www.press.bmwgroup.com/asia/article/detail/T0046588EN/the-bmw-gina-light-visionary-model-innovative-approach-and-optical-expression-of-creative-freedom?language=en", "Estudo revelado em 2008 que substituiu painéis convencionais por uma pele têxtil flexível sobre estrutura móvel, investigando forma adaptável e novos limites entre material, função e superfície."),
    "BMW Vision EfficientDynamics": ("promote-editorial", "BMW Vision EfficientDynamics", "BMW Group", "https://www.press.bmwgroup.com/global/article/detail/T0039554EN/bmw-vision-efficientdynamics?language=en", "Conceito híbrido plug-in apresentado em 2009 como integração de desempenho esportivo, aerodinâmica, construção leve e eletrificação no programa EfficientDynamics."),
    "Porsche 918 Spyder Concept": ("promote-editorial", "10 years of the Porsche 918 Spyder", "Porsche Newsroom", "https://newsroom.porsche.com/en/press-kits/Media-Drive-Cayenne-E-Performance/10-Jahre-Porsche-918-Spyder.html", "Conceito híbrido plug-in apresentado em 2010 e desenvolvido até o 918 Spyder de série limitada, combinando desempenho de superesportivo e estratégias de eletrificação."),
    "Porsche Mission E": ("promote-editorial", "Mission E becomes Taycan", "Porsche Newsroom", "https://newsroom.porsche.com/en/products/porsche-taycan-mission-e-name-of-series-production-electric-sports-car-electromobility-concept-study-70-years-sportscar-15602.html", "Conceito elétrico revelado em 2015 que foi aprovado para desenvolvimento e tornou-se o Taycan, estabelecendo uma linhagem nominal e industrial verificável entre estudo e produção."),
}


def main() -> None:
    db = sqlite3.connect(DB)
    try:
        for name, (decision, title, publisher, url, description) in RECORDS.items():
            row = db.execute("SELECT id, metadata_json FROM entity WHERE canonical_name=?", (name,)).fetchone()
            if not row:
                raise ValueError(f"candidate not found: {name}")
            source_id = stable_uuid7("source:" + url)
            db.execute(
                """INSERT INTO source(id,source_type,title,publisher,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at)
                VALUES(?,'manufacturer_archive',?,?,?,'2026-08-25','en','A','{}','Fonte da revisão CP19 C05.',?,?)
                ON CONFLICT(id) DO UPDATE SET title=excluded.title,publisher=excluded.publisher,accessed_at=excluded.accessed_at,updated_at=excluded.updated_at""",
                (source_id, title, publisher, url, NOW, NOW),
            )
            metadata = json.loads(row[1] or "{}")
            slug = name.lower().replace(" ", "-").replace("/", "-")
            metadata.update({
                "curation_batch": "C05", "curation_review": f"atlas:curation-review:c05-{slug}",
                "curation_reviewed_at": "2026-08-25", "curation_decision": decision,
                "curation_source_ids": [source_id], "editorial_level": "catalog",
                "promotion_state": "approved_pending_v2_cut" if decision == "promote-editorial" else "retained_catalog_after_review",
                "verification_state": "source_backed", "verified_at": "2026-08-25",
            })
            db.execute("UPDATE entity SET description=?, metadata_json=?, updated_at=? WHERE id=?",
                       (description, json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, row[0]))
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    promote = sum(value[0] == "promote-editorial" for value in RECORDS.values())
    print(json.dumps({"batch": "C05", "reviewed": len(RECORDS), "promote": promote, "retain": len(RECORDS) - promote}))


if __name__ == "__main__":
    main()
