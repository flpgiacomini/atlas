#!/usr/bin/env python3
"""Apply CP19 C04 sources and reviewed decisions to the transition database."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from enrich_people_batch_01 import stable_uuid7

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
NOW = "2026-08-25T20:00:00+00:00"

RECORDS = {
    "BMW Turbo": ("promote-editorial", "BMW Design concept cars", "BMW Group", "https://www.press.bmwgroup.com/global/article/detail/T0135428EN/bmw-design-concept-cars", "Primeiro concept car da BMW, apresentado em 1972 como laboratório de segurança, aerodinâmica e ergonomia para um esportivo. Sua relevância editorial está na transferência declarada de soluções para modelos posteriores."),
    "Volvo VESC": ("promote-editorial", "Volvo Experimental Safety Car (VESC), 1972", "Volvo Cars", "https://www.volvocars.com/intl/media/models/vesc/1972/", "Experimental Safety Car de 1972 que reuniu soluções de proteção, visibilidade e emissões. A Volvo o identifica como precursor direto do programa de segurança materializado no 240."),
    "Hyundai Pony Coupe Concept": ("promote-editorial", "Hyundai Motor and Giorgetto Giugiaro collaborate to rebuild original 1974 Pony Coupe Concept", "Hyundai Motor Company", "https://www.hyundai.com/content/hyundai/ww/data/news/data/2022/0000016922/attach/%28Press%20Release%29%20Hyundai%20Motor%20and%20Legendary%20Designer%20Giorgetto%20Giugiaro%20Collaborate%20to%20Rebuild%20Original%201974%20Pony%20Coupe%20Concept.pdf", "Conceito desenhado por Giorgetto Giugiaro e apresentado em Turim em 1974. Documenta a formação de uma linguagem própria para o primeiro programa automotivo independente da Hyundai e sua recuperação posterior pela marca."),
    "Italdesign Megagamma": ("promote-editorial", "Megagamma", "Italdesign", "https://www.italdesign.it/en/project/megagamma/", "Estudo de 1978 sobre base Lancia Gamma que reorganizou altura, espaço interno e embalagem mecânica em um monovolume compacto concebido como proposta industrial realizável."),
    "Ford Probe III": ("retain-catalog", "Ford Heritage Vault", "Ford Motor Company", "https://www.fordheritagevault.com/", "Conceito europeu de 1981 mantido no catálogo. A revisão não localizou no arquivo institucional consultado uma ficha individual capaz de sustentar, sem fonte secundária, a influência historicamente atribuída ao Sierra."),
    "Peugeot Quasar": ("promote-editorial", "1984: Peugeot, Lancia, la 205 e sogna con la Quasar", "Peugeot / Stellantis", "https://www.media.stellantis.com/it-it/peugeot/press/1984-peugeot-lancia-la-205-e-sogna-con-la-quasar", "Primeiro grande concept car da Peugeot, revelado em 1984 como demonstração conjunta de desenho, eletrônica embarcada e mecânica derivada da competição."),
    "Nissan MID4": ("promote-editorial", "Nissan MID4 Type II", "Nissan Motor Corporation", "https://www.nissan-global.com/EN/HERITAGE_COLLECTION/nissan_mid_4_type_ii.html", "Programa experimental iniciado em 1985 para motor central e tração integral. O arquivo Nissan registra a transferência de tecnologias desenvolvidas no MID4 para o 300ZX Z32 e o Skyline GT-R R32."),
    "Peugeot Proxima": ("retain-catalog", "The collection of L'Aventure Peugeot", "L'Aventure Peugeot Citroën DS", "https://laventure-association.com/en/the-collection-of-laventure-peugeot/", "Conceito de 1986 preservado no catálogo. A coleção institucional confirma a preservação do patrimônio conceitual, mas a revisão não encontrou uma ficha individual suficiente para demonstrar consequência histórica específica."),
    "Peugeot Oxia": ("retain-catalog", "The collection of L'Aventure Peugeot", "L'Aventure Peugeot Citroën DS", "https://laventure-association.com/en/the-collection-of-laventure-peugeot/", "Conceito de 1988 preservado no catálogo. Sem uma ficha institucional individual que documente transferência, adoção ou linhagem posterior, a notoriedade do exemplar não basta para promoção editorial."),
    "Porsche 989": ("promote-editorial", "Four wins – sports car with four seats", "Porsche Newsroom", "https://newsroom.porsche.com/en/2019/history/porsche-four-wins-sports-car-four-seats-18908.html", "Protótipo de sedã esportivo de quatro portas desenvolvido a partir de 1988 e cancelado por razões econômicas. O arquivo Porsche o situa na genealogia de estudos que antecederam o Panamera."),
    "GM Impact": ("promote-editorial", "1990 Impact Experimental", "General Motors Heritage Collection", "https://www.gm.com/heritage/collection/gm-concept/1990-impact-experimental", "Demonstrador elétrico apresentado em 1990 cuja tecnologia e resposta pública deram origem ao programa de produção GM EV1."),
    "Audi Avus quattro": ("promote-editorial", "Audi anniversary dates 2021", "Audi MediaCenter", "https://www.audi-mediacenter.com/en/publications/more/audi-anniversary-dates-2021-1016/download", "Superesportivo conceitual apresentado em Tóquio em 1991 para demonstrar a construção leve em alumínio e uma arquitetura W12, consolidando publicamente tecnologias centrais da Audi dos anos 1990."),
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
                VALUES(?,'manufacturer_archive',?,?,?,'2026-08-25','en','A','{}','Fonte da revisão CP19 C04.',?,?)
                ON CONFLICT(id) DO UPDATE SET title=excluded.title,publisher=excluded.publisher,accessed_at=excluded.accessed_at,updated_at=excluded.updated_at""",
                (source_id, title, publisher, url, NOW, NOW),
            )
            metadata = json.loads(row[1] or "{}")
            slug = name.lower().replace(" ", "-").replace("/", "-")
            metadata.update({
                "curation_batch": "C04", "curation_review": f"atlas:curation-review:c04-{slug}",
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
    print(json.dumps({"batch": "C04", "reviewed": len(RECORDS), "promote": promote, "retain": len(RECORDS) - promote}))


if __name__ == "__main__":
    main()
