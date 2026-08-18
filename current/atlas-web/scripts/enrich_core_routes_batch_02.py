#!/usr/bin/env python3
"""Idempotent narrative enrichment for the five core vehicle routes."""

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOW = "2026-08-18T18:30:00+00:00"

DESCRIPTIONS = {
    "Benz Patent Motor Car": "Família do automóvel patenteado por Carl Benz em 1886, concebida desde o início como veículo movido por motor a combustão, e não como adaptação de uma carruagem. Representa um marco fundador da história técnica e industrial do automóvel.",
    "Ford Model T": "Automóvel produzido pela Ford Motor Company entre 1908 e 1927 que combinou materiais resistentes, projeto funcional e fabricação em escala crescente. Sua trajetória entre Piquette Avenue e Highland Park ajuda a explicar a transformação do carro em bem de consumo de massa.",
    "Porsche 911": "Família de esportivos apresentada originalmente como Porsche 901 e rebatizada 911 em 1964. Desenvolvida como sucessora do 356, recebeu o desenho de Ferdinand Alexander Porsche e consolidou uma linhagem técnica e visual continuamente reinterpretada ao longo de oito gerações.",
    "Porsche 917": "Protótipo de competição criado pela Porsche para enfrentar o regulamento internacional de carros esporte no fim dos anos 1960. Com motor de doze cilindros e múltiplas configurações aerodinâmicas, tornou-se protagonista das vitórias gerais da marca em Le Mans.",
    "Volvo PV544": "Automóvel de passageiros da Volvo associado à introdução em série do cinto de segurança moderno de três pontos em 1959. O modelo funciona no Atlas como elo entre engenharia de produto, pesquisa de segurança e disseminação de uma tecnologia de proteção mundialmente adotada.",
}


def main() -> None:
    db = sqlite3.connect(ROOT / "data" / "atlas.sqlite")
    changed = 0
    try:
        for name, description in DESCRIPTIONS.items():
            row = db.execute("SELECT id FROM entity WHERE canonical_name=?", (name,)).fetchone()
            if not row:
                raise ValueError(f"Missing entity: {name}")
            result = db.execute(
                "UPDATE entity SET description=?, updated_at=? WHERE id=? AND coalesce(description,'')<>?",
                (description, NOW, row[0], description),
            )
            changed += result.rowcount
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    print(json.dumps({"routes_enriched": len(DESCRIPTIONS), "rows_changed": changed, "status": "ok"}))


if __name__ == "__main__":
    main()
