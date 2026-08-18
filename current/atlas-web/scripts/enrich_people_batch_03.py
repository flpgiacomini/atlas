#!/usr/bin/env python3
"""Idempotent enrichment for roadmap batch E03."""

import json
import sqlite3
from pathlib import Path

from enrich_people_batch_01 import add_statement, stable_uuid7

ROOT = Path(__file__).resolve().parents[1]
NOW = "2026-08-18T19:30:00+00:00"

PEOPLE = {
    "Alec Issigonis": ("Engenheiro e projetista britânico de origem grega, responsável pelo conceito do Classic Mini. Seu arranjo transversal com tração dianteira privilegiou o espaço interno e transformou o pequeno automóvel apresentado pela British Motor Corporation em 1959.", "Q457634", "1906-11-18", "1988-10-02"),
    "Armand Peugeot": ("Industrial francês e pioneiro da motorização que conduziu a família Peugeot da fabricação de bens metálicos à produção de veículos. Participou do desenvolvimento dos primeiros automóveis da marca e estabeleceu uma atividade industrial dedicada ao setor.", "Q1388558", "1849-03-26", "1915-01-02"),
    "Charles Rolls": ("Pioneiro britânico do automobilismo e da aviação, comerciante de automóveis e cofundador da empresa associada a Henry Royce. O encontro entre ambos, em 1904, reuniu a capacidade comercial de Rolls à engenharia e fabricação de Royce.", "Q313074", "1877-08-27", "1910-07-12"),
    "Claudio Fogolin": ("Empresário e ciclista italiano que se associou a Vincenzo Lancia na criação da Lancia & C. em Turim. Participou da formação administrativa da companhia durante seus primeiros anos, enquanto Lancia liderava o desenvolvimento técnico dos automóveis.", "Q15976363", "1872", "1945"),
    "Emil Jellinek": ("Empresário e entusiasta do automobilismo ligado à Daimler-Motoren-Gesellschaft, para a qual promoveu e encomendou automóveis de alto desempenho. O nome Mercedes, inspirado em sua filha, tornou-se a identidade comercial dos veículos negociados por ele.", "Q78589", "1853-04-06", "1918-01-21"),
    "Ferenc Szisz": ("Mecânico e piloto húngaro ligado à Renault, vencedor do primeiro Grand Prix de l’A.C.F. em 1906. Sua atuação combinou preparação técnica e condução em prova, tornando-o personagem central da consolidação inicial das corridas de Grande Prêmio.", "Q918792", "1873-09-20", "1944-02-21"),
    "Fernand Renault": ("Empresário francês que fundou a Renault Frères com os irmãos Louis e Marcel. Atuou na organização comercial e industrial da companhia durante sua fase pioneira, quando os primeiros veículos Renault ganharam mercado e participaram de competições.", "Q729431", "1864-11-28", "1909-03-22"),
    "George Heath": ("Piloto nascido nos Estados Unidos e associado às competições automobilísticas francesas, vencedor da primeira Vanderbilt Cup em 1904 ao volante de um Panhard. Sua vitória conectou a experiência europeia às primeiras grandes provas organizadas nos Estados Unidos.", None, None, None),
    "Georges Bouton": ("Engenheiro francês e cofundador da De Dion-Bouton, responsável por importantes experiências com motores leves no fim do século XIX. Seu trabalho no motor monocilíndrico a petróleo ajudou a ampliar a aplicação prática da propulsão automotiva.", "Q5546759", "1847-11-22", "1938-10-31"),
}

PIECH_DESCRIPTION = "Engenheiro e executivo austríaco que iniciou a carreira na Porsche em 1963, chefiou testes e desenvolvimento e liderou o programa do 917. Posteriormente transferiu-se para a Audi, mantendo longa participação no conselho supervisor da Porsche."


def source(db, qid):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
    sid = stable_uuid7(f"source:{url}")
    db.execute("""INSERT OR IGNORE INTO source
      (id,source_type,title,author,publisher,published_at,url,accessed_at,language,source_tier,zotero_key,external_ids_json,notes,created_at,updated_at)
      VALUES (?,'structured_data',?,NULL,'Wikidata',NULL,?,'2026-08-18','mul','B',NULL,?,? ,?,?)""",
      (sid, f"Wikidata entity {qid}", url, json.dumps({"wikidata": qid}), "Datas vitais verificadas no registro estruturado; carreira confrontada com fonte institucional do Atlas.", NOW, NOW))
    return sid


def main():
    db = sqlite3.connect(ROOT / "data" / "atlas.sqlite")
    db.execute("PRAGMA foreign_keys=ON")
    try:
        for name, (description, qid, born, died) in PEOPLE.items():
            db.execute("UPDATE entity SET description=?,updated_at=? WHERE canonical_name=?", (description, NOW, name))
            if not qid:
                continue
            sid = source(db, qid)
            add_statement(db, name, sid, ("born_on", "date", born, "year" if len(born) == 4 else "day", None, None))
            add_statement(db, name, sid, ("died_on", "date", died, "year" if len(died) == 4 else "day", None, None))

        piech_url = "https://newsroom.porsche.com/en/2019/company/porsche-obituary-ferdinand-piech-18460.html"
        piech_sid = stable_uuid7(f"source:{piech_url}")
        db.execute("UPDATE entity SET description=?,updated_at=? WHERE canonical_name='Ferdinand Piëch'", (PIECH_DESCRIPTION, NOW))
        db.execute("""INSERT OR IGNORE INTO source
          (id,source_type,title,author,publisher,published_at,url,accessed_at,language,source_tier,zotero_key,external_ids_json,notes,created_at,updated_at)
          VALUES (?,'institutional','Porsche mourns the death of Ferdinand Piëch',NULL,'Porsche Newsroom','2019-08-27',?,'2026-08-18','en','A',NULL,'{}','Obituário institucional com cronologia profissional.',?,?)""", (piech_sid, piech_url, NOW, NOW))
        for spec in [
            ("died_on", "date", "2019-08-25", "day", None, None),
            ("worked_at", "entity", "Dr. Ing. h.c. F. Porsche AG", None, "1963-04-01", "day"),
            ("led", "entity", "Dr. Ing. h.c. F. Porsche AG", None, "1966", "year"),
        ]:
            add_statement(db, "Ferdinand Piëch", piech_sid, spec)
        db.commit()
    except Exception:
        db.rollback(); raise
    finally:
        db.close()
    print(json.dumps({"batch":"E03","descriptions":10,"statements":19,"status":"researched_with_one_declared_gap"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
