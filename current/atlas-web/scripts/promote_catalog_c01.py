#!/usr/bin/env python3
"""Promote the six source-backed CP19 C01 candidates after editorial review."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
NOW = "2026-08-25T15:00:00+00:00"
REVIEWS = {
    "Aston Martin Bulldog": "atlas:curation-review:c01-aston-martin-bulldog",
    "Chrysler Turbine Car": "atlas:curation-review:c01-chrysler-turbine-car",
    "Ferrari P4/5 by Pininfarina": "atlas:curation-review:c01-ferrari-p4-5",
    "Maybach Exelero": "atlas:curation-review:c01-maybach-exelero",
    "Mercedes-Benz C 111": "atlas:curation-review:c01-mercedes-benz-c-111",
    "Volkswagen W12": "atlas:curation-review:c01-volkswagen-w12",
}


def main() -> None:
    db = sqlite3.connect(DB)
    try:
        promoted = 0
        for name, review in REVIEWS.items():
            row = db.execute("SELECT id, metadata_json FROM entity WHERE canonical_name=?", (name,)).fetchone()
            if not row:
                raise ValueError(f"candidate not found: {name}")
            metadata = json.loads(row[1] or "{}")
            if metadata.get("verification_state") != "source_backed":
                raise ValueError(f"candidate lacks source-backed verification: {name}")
            metadata.update({
                "editorial_level": "catalog",
                "promotion_state": "approved_pending_v2_cut",
                "curation_decision": "promote-editorial",
                "curation_review": review,
                "curation_batch": "C01",
                "curation_reviewed_at": "2026-08-25",
            })
            db.execute(
                "UPDATE entity SET metadata_json=?, updated_at=? WHERE id=?",
                (json.dumps(metadata, ensure_ascii=False, sort_keys=True), NOW, row[0]),
            )
            promoted += 1
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    print(json.dumps({"batch": "C01", "promoted": promoted, "reviews": len(REVIEWS)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
