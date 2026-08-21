"""Deterministically project the Atlas v1 SQLite corpus into v2 documents."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sqlite3
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT.parent / "atlas-web" / "data" / "atlas.sqlite"
DEFAULT_OUTPUT = ROOT / "migration"
CONTEXT = "https://flpgiacomini.github.io/atlas/context/v2.jsonld"

TYPE_MAP = {
    "brand": "Brand", "vehicle": "Vehicle", "event": "Event",
    "person": "Person", "technology": "Technology",
    "organization": "Organization", "facility": "Facility",
    "component": "Component", "circuit_layout": "CircuitLayout",
    "vehicle_instance": "VehicleInstance", "circuit": "Circuit",
    "competition": "Series", "entry": "Entry", "place": "Place",
    "team": "Team",
}
TRUST_MAP = {"A": "primary", "B": "institutional", "C": "specialist", "D": "context"}


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
    return slug or "unnamed"


def json_value(value: str | None, fallback):
    if not value:
        return fallback
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return fallback


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rows(connection: sqlite3.Connection, query: str) -> list[dict]:
    return [dict(row) for row in connection.execute(query)]


def build_ids(records: list[dict], kind_key: str, name_key: str) -> dict[str, str]:
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for record in records:
        grouped[(slugify(str(record[kind_key])), slugify(str(record[name_key])))].append(record)
    result: dict[str, str] = {}
    for (kind, base), group in sorted(grouped.items()):
        for index, record in enumerate(sorted(group, key=lambda item: item["id"])):
            suffix = "" if index == 0 else f"-{record['id'].replace('-', '')[:8]}"
            result[record["id"]] = f"atlas:{kind}:{base}{suffix}"
    return result


def source_document(record: dict, semantic_id: str) -> dict:
    result = {
        "id": semantic_id,
        "type": "Source",
        "title": record["title"],
        "trust": TRUST_MAP.get(record.get("source_tier"), "context"),
        "legacyId": record["id"],
        "sourceType": record["source_type"],
    }
    for old, new in (("author", "author"), ("publisher", "publisher"), ("url", "url"),
                     ("published_at", "publishedAt"), ("accessed_at", "verifiedAt"),
                     ("language", "language"), ("zotero_key", "zoteroKey"), ("notes", "notes")):
        if record.get(old) is not None:
            result[new] = record[old]
    external = json_value(record.get("external_ids_json"), {})
    if external:
        result["externalIds"] = external
    return result


def statement_object(statement: dict, entity_ids: dict[str, str]):
    object_type = statement["object_type"]
    if object_type == "entity":
        return {"id": entity_ids[statement["object_entity_id"]], "type": "EntityReference"}
    if object_type == "number":
        result = {"value": statement["object_number"], "type": "number"}
        if statement.get("object_unit"):
            result["unit"] = statement["object_unit"]
        return result
    if object_type == "date":
        return {"value": statement["object_date"], "type": "date", "precision": statement.get("object_date_precision") or "unknown"}
    if object_type == "boolean":
        return bool(statement["object_boolean"])
    return statement.get("object_text")


def validity(statement: dict) -> dict | None:
    if not statement.get("valid_from") and not statement.get("valid_until"):
        return None
    result = {
        "from": statement.get("valid_from"),
        "until": statement.get("valid_until"),
        "precision": statement.get("valid_from_precision") or statement.get("valid_until_precision") or "unknown",
    }
    return result


def migrate(database: Path, output: Path) -> dict:
    if not database.is_file():
        raise FileNotFoundError(database)
    temp = output.with_name(output.name + ".tmp")
    if temp.exists():
        shutil.rmtree(temp)
    temp.mkdir(parents=True)

    connection = sqlite3.connect(f"file:{database.as_posix()}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    entities = rows(connection, "SELECT * FROM entity ORDER BY id")
    names = rows(connection, "SELECT * FROM entity_name ORDER BY entity_id, value, id")
    external_ids = rows(connection, "SELECT * FROM external_identifier ORDER BY entity_id, scheme, value, id")
    sources = rows(connection, "SELECT * FROM source ORDER BY id")
    predicate_records = rows(connection, "SELECT * FROM predicate ORDER BY id")
    predicates = {row["id"]: row["name"] for row in predicate_records}
    statements = {row["id"]: row for row in rows(connection, "SELECT * FROM statement ORDER BY id")}
    claims = rows(connection, "SELECT * FROM claim ORDER BY id")
    evidence = {row["id"]: row for row in rows(connection, "SELECT * FROM evidence ORDER BY id")}
    claim_evidence: dict[str, list[str]] = defaultdict(list)
    for row in rows(connection, "SELECT * FROM claim_evidence ORDER BY claim_id, evidence_id"):
        claim_evidence[row["claim_id"]].append(row["evidence_id"])
    redirects = rows(connection, "SELECT * FROM entity_redirect ORDER BY old_entity_id")
    legacy = rows(connection, "SELECT * FROM legacy_identifier ORDER BY legacy_id")
    connection.close()

    entity_ids = build_ids(
        [{**record, "kind": record["entity_type"]} for record in entities], "kind", "canonical_name"
    )
    source_ids = build_ids(
        [{**record, "kind": "source", "display": f"{record.get('publisher') or ''}-{record['title']}"} for record in sources],
        "kind", "display",
    )
    evidence_ids = {old: f"atlas:evidence:legacy-{old.replace('-', '')}" for old in evidence}
    claim_ids = {record["id"]: f"atlas:claim:legacy-{record['id'].replace('-', '')}" for record in claims}

    names_by_entity: dict[str, list[dict]] = defaultdict(list)
    for row in names:
        names_by_entity[row["entity_id"]].append(row)
    external_by_entity: dict[str, list[dict]] = defaultdict(list)
    for row in external_ids:
        external_by_entity[row["entity_id"]].append(row)
    claims_by_entity: dict[str, list[dict]] = defaultdict(list)

    evidence_documents = []
    for old_id, record in sorted(evidence.items()):
        doc = {
            "id": evidence_ids[old_id], "type": "Evidence", "legacyId": old_id,
            "source": source_ids[record["source_id"]], "evidenceType": record["evidence_type"],
            "locator": json_value(record.get("locator_json"), {}),
        }
        if record.get("excerpt") is not None:
            doc["excerpt"] = record["excerpt"]
        if record.get("notes") is not None:
            doc["notes"] = record["notes"]
        evidence_documents.append(doc)

    for claim in claims:
        statement = statements[claim["statement_id"]]
        evidence_refs = claim_evidence[claim["id"]]
        source_refs = sorted({source_ids[evidence[eid]["source_id"]] for eid in evidence_refs})
        doc = {
            "id": claim_ids[claim["id"]], "type": "Claim", "legacyId": claim["id"],
            "statementLegacyId": statement["id"], "subject": entity_ids[statement["subject_entity_id"]],
            "predicate": predicates[statement["predicate_id"]].replace("_", "-"),
            "object": statement_object(statement, entity_ids), "sources": source_refs,
            "evidence": [evidence_ids[eid] for eid in evidence_refs], "stance": claim["stance"],
            "supportStrength": claim["support_strength"], "confidence": statement["confidence"],
            "resolutionStatus": statement["resolution_status"],
        }
        interval = validity(statement)
        if interval:
            doc["validity"] = interval
        qualifiers = json_value(statement.get("qualifiers_json"), {})
        if qualifiers:
            doc["qualifiers"] = qualifiers
        if claim.get("note") is not None:
            doc["note"] = claim["note"]
        claims_by_entity[statement["subject_entity_id"]].append(doc)

    for entity in entities:
        semantic_id = entity_ids[entity["id"]]
        aliases = sorted({row["value"] for row in names_by_entity[entity["id"]] if row["value"] != entity["canonical_name"]})
        doc = {
            "@context": CONTEXT, "id": semantic_id,
            "type": TYPE_MAP.get(entity["entity_type"], "Entity"),
            "name": entity["canonical_name"], "aliases": aliases,
            "claims": sorted(claims_by_entity[entity["id"]], key=lambda item: item["id"]),
            "legacy": {"id": entity["id"], "type": entity["entity_type"], "slug": entity.get("slug")},
            "names": [
                {key: row[key] for key in ("id", "value", "name_type", "language", "valid_from", "valid_from_precision", "valid_until", "valid_until_precision", "source_note") if row.get(key) is not None}
                for row in names_by_entity[entity["id"]]
            ],
        }
        if entity.get("description"):
            doc["description"] = entity["description"]
        metadata = json_value(entity.get("metadata_json"), {})
        if metadata:
            doc["metadata"] = metadata
        if external_by_entity[entity["id"]]:
            doc["externalIds"] = [
                {key: row[key] for key in ("id", "scheme", "value", "url") if row.get(key) is not None}
                for row in external_by_entity[entity["id"]]
            ]
        _, semantic_type, semantic_slug = semantic_id.split(":", 2)
        dump(temp / "entities" / f"{semantic_type}--{semantic_slug}.jsonld", doc)

    source_documents = [source_document(record, source_ids[record["id"]]) for record in sources]
    dump(temp / "sources.jsonld", {"@context": CONTEXT, "type": "SourceCollection", "items": source_documents})
    dump(temp / "evidence.jsonld", {"@context": CONTEXT, "type": "EvidenceCollection", "items": evidence_documents})
    dump(temp / "predicates.jsonld", {
        "@context": CONTEXT,
        "type": "PredicateCollection",
        "items": [
            {
                "id": f"atlas:predicate:{slugify(row['name'])}", "type": "Predicate",
                "legacyId": row["id"], "name": row["name"], "description": row["description"],
                "subjectTypes": json_value(row["subject_types_json"], []),
                "objectTypes": json_value(row["object_types_json"], []),
                "temporalPolicy": row["temporal_policy"], "symmetric": bool(row["symmetric"]),
                "status": row["status"],
            }
            for row in predicate_records
        ],
    })
    dump(temp / "identity-map.json", {
        "version": "2.0.0", "entities": dict(sorted(entity_ids.items())),
        "sources": dict(sorted(source_ids.items())), "claims": dict(sorted(claim_ids.items())),
        "evidence": dict(sorted(evidence_ids.items())), "redirects": redirects, "legacyIdentifiers": legacy,
    })
    report = {
        "version": "2.0.0", "databaseSha256": hashlib.sha256(database.read_bytes()).hexdigest(),
        "counts": {"entities": len(entities), "statements": len(statements), "claims": len(claims),
                   "sources": len(sources), "evidence": len(evidence), "redirects": len(redirects),
                   "legacyIdentifiers": len(legacy), "entityNames": len(names),
                   "externalIdentifiers": len(external_ids), "predicates": len(predicate_records)},
        "documents": {"entityFiles": len(entities), "sourceItems": len(source_documents),
                      "evidenceItems": len(evidence_documents)},
        "status": "migration-candidate",
    }
    dump(temp / "migration-report.json", report)
    checksums = {}
    for path in sorted(temp.rglob("*")):
        if path.is_file():
            checksums[path.relative_to(temp).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    dump(temp / "checksums.json", {"algorithm": "sha256", "files": checksums})
    if output.exists():
        shutil.rmtree(output)
    temp.replace(output)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", type=Path, default=DEFAULT_DB)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(migrate(args.database.resolve(), args.output.resolve()), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
