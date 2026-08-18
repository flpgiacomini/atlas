"""Prepare the canonical statement projection for Heurist's CSV importer."""

from __future__ import annotations

import csv
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "statements_for_heurist.csv"
TARGET = HERE / "statements_for_heurist_import.csv"


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))

    fieldnames = [
        "statement_id",
        "subject_atlas_id",
        "predicate",
        "object_type",
        "object_entity_atlas_id",
        "literal_value",
        "object_precision",
        "valid_from",
        "valid_from_precision",
        "valid_until",
        "valid_until_precision",
        "qualifiers_json",
        "confidence_label",
        "resolution_status",
        "source_ids",
    ]
    prepared = []
    for row in rows:
        is_entity = row["object_type"] == "entity"
        prepared.append(
            {
                "statement_id": row["statement_id"],
                "subject_atlas_id": row["subject_atlas_id"],
                "predicate": row["predicate"],
                "object_type": row["object_type"],
                "object_entity_atlas_id": row["object_value"] if is_entity else "",
                "literal_value": "" if is_entity else row["object_value"],
                "object_precision": row["object_precision"],
                "valid_from": row["valid_from"],
                "valid_from_precision": row["valid_from_precision"],
                "valid_until": row["valid_until"],
                "valid_until_precision": row["valid_until_precision"],
                "qualifiers_json": row["qualifiers_json"],
                "confidence_label": row["confidence"],
                "resolution_status": row["resolution_status"],
                "source_ids": row["source_ids"].replace(",", "|"),
            }
        )

    with TARGET.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(prepared)

    print(f"Prepared {len(prepared)} statements at {TARGET}")


if __name__ == "__main__":
    main()
