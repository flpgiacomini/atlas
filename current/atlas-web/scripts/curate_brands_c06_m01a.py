#!/usr/bin/env python3
"""Apply CP19 C06/M01A sources and reviewed brand decisions."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from enrich_people_batch_01 import stable_uuid7

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
NOW = "2026-08-25T22:00:00+00:00"

RECORDS = {
    "Benz": (
        "Beginnings of the automobile: The predecessor companies (1886–1920)", "Mercedes-Benz Group",
        "https://group.mercedes-benz.com/company/tradition/company-history/1886-1920.html",
        "Marca ligada à empresa fundada por Carl Benz em Mannheim e à exploração industrial do automóvel patenteado em 1886. Sua trajetória desemboca na fusão com a Daimler-Motoren-Gesellschaft em 1926."),
    "Daimler": (
        "Beginnings of the automobile: The predecessor companies (1886–1920)", "Mercedes-Benz Group",
        "https://group.mercedes-benz.com/company/tradition/company-history/1886-1920.html",
        "Marca e linhagem industrial associadas a Gottlieb Daimler, Wilhelm Maybach e à Daimler-Motoren-Gesellschaft. A documentação registra sua origem independente e a convergência posterior com Benz."),
    "Mercedes-Benz": (
        "Tradition, transformation and technology leadership: 100 years of Mercedes-Benz", "Mercedes-Benz Group",
        "https://group.mercedes-benz.com/unternehmen/tradition/geschichte/100-jahre-marke-mb.html",
        "Marca formada em 1926 pela reunião das tradições Daimler e Benz. O nome, o emblema e o primeiro programa comum documentam uma das principais consolidações da indústria automotiva."),
    "Ford": (
        "Ford Company Timeline", "Ford Motor Company",
        "https://corporate.ford.com/about/history/company-timeline/",
        "Marca fundada em 1903 cuja história conecta o Model T, a expansão internacional e a linha de montagem móvel. Sua contribuição central é a reorganização industrial e econômica da produção em massa."),
    "De Dion-Bouton": (
        "Storia della De Dion Bouton", "Museo Nazionale dell'Automobile",
        "https://www.museoauto.com/qrcode/storia-della-de-dion-bouton/",
        "Fabricante pioneira fundada no ciclo do vapor e depois decisiva na difusão de pequenos motores de combustão e do eixo De Dion. O museu registra sua escala mundial por volta de 1900 e o encerramento em 1933."),
    "Panhard & Levassor": (
        "Panhard and Levassor", "Science Museum Group",
        "https://collection.sciencemuseumgroup.org.uk/people/cp61124/panhard-and-levassor",
        "Fabricante francesa pioneira que produziu motores Daimler sob licença e participou da definição do automóvel de motor dianteiro e tração traseira. Sua produção inicial e atividade esportiva ajudam a explicar a consolidação do carro prático."),
}


def main() -> None:
    db = sqlite3.connect(DB)
    try:
        for name, (title, publisher, url, description) in RECORDS.items():
            row = db.execute("SELECT id, metadata_json FROM entity WHERE canonical_name=? AND entity_type='brand'", (name,)).fetchone()
            if not row:
                raise ValueError(f"brand candidate not found: {name}")
            existing = db.execute("SELECT id FROM source WHERE url=? ORDER BY id LIMIT 1", (url,)).fetchone()
            source_id = existing[0] if existing else stable_uuid7("source:" + url)
            db.execute(
                """INSERT INTO source(id,source_type,title,publisher,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at)
                VALUES(?,'institutional',?,?,?,'2026-08-25','en','A','{}','Fonte da revisão CP19 C06/M01A.',?,?)
                ON CONFLICT(id) DO UPDATE SET title=excluded.title,publisher=excluded.publisher,accessed_at=excluded.accessed_at,updated_at=excluded.updated_at""",
                (source_id, title, publisher, url, NOW, NOW),
            )
            metadata = json.loads(row[1] or "{}")
            slug = name.lower().replace(" ", "-").replace("&", "and")
            metadata.update({
                "curation_batch": "C06-M01A", "curation_review": f"atlas:curation-review:c06-{slug}",
                "curation_reviewed_at": "2026-08-25", "curation_decision": "promote-editorial",
                "curation_source_ids": [source_id], "editorial_level": "catalog",
                "promotion_state": "approved_pending_v2_cut", "verification_state": "source_backed",
                "verified_at": "2026-08-25",
            })
            db.execute("UPDATE entity SET description=?, metadata_json=?, updated_at=? WHERE id=?",
                       (description, json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, row[0]))
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    print(json.dumps({"batch": "C06-M01A", "reviewed": len(RECORDS), "promote": len(RECORDS), "retain": 0}))


if __name__ == "__main__":
    main()
