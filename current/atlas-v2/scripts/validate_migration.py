"""Validate lossless references and deterministic checksums in a v2 migration."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT.parent / "atlas-web" / "data" / "atlas.sqlite"
DEFAULT_MIGRATION = ROOT / "migration"
ID = re.compile(r"^atlas:[a-z][a-z0-9-]*:[a-z0-9]+(?:-[a-z0-9]+)*$")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def table_count(connection: sqlite3.Connection, table: str) -> int:
    return connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def validate(database: Path, migration: Path) -> dict:
    report = load(migration / "migration-report.json")
    identity = load(migration / "identity-map.json")
    sources = load(migration / "sources.jsonld")["items"]
    evidence = load(migration / "evidence.jsonld")["items"]
    predicates = load(migration / "predicates.jsonld")["items"]
    entity_files = sorted((migration / "entities").glob("*.jsonld"))
    entities = [load(path) for path in entity_files]
    claims = [claim for entity in entities for claim in entity["claims"]]

    connection = sqlite3.connect(f"file:{database.as_posix()}?mode=ro", uri=True)
    expected = {table: table_count(connection, table) for table in ("entity", "entity_name", "external_identifier", "statement", "claim", "source", "evidence", "predicate", "entity_redirect", "legacy_identifier")}
    connection.close()
    actual = {
        "entity": len(entities), "claim": len(claims), "source": len(sources), "evidence": len(evidence),
        "entity_redirect": len(identity["redirects"]), "legacy_identifier": len(identity["legacyIdentifiers"]),
        "statement": len({claim["statementLegacyId"] for claim in claims}),
        "entity_name": sum(len(entity.get("names", [])) for entity in entities),
        "external_identifier": sum(len(entity.get("externalIds", [])) for entity in entities),
        "predicate": len(predicates),
    }
    if expected != actual:
        raise ValueError(f"loss detected: expected={expected}, actual={actual}")

    ids = {entity["id"] for entity in entities} | {source["id"] for source in sources} | {item["id"] for item in evidence} | {claim["id"] for claim in claims}
    invalid_ids = sorted(value for value in ids if not ID.fullmatch(value))
    if invalid_ids:
        raise ValueError(f"invalid semantic IDs: {invalid_ids[:5]}")
    if len(ids) != len(entities) + len(sources) + len(evidence) + len(claims):
        raise ValueError("semantic ID collision")

    entity_ids = {entity["id"] for entity in entities}
    source_ids = {source["id"] for source in sources}
    evidence_ids = {item["id"] for item in evidence}
    for claim in claims:
        if claim["subject"] not in entity_ids:
            raise ValueError(f"unresolved subject: {claim['id']}")
        if any(source not in source_ids for source in claim["sources"]):
            raise ValueError(f"unresolved source: {claim['id']}")
        if any(item not in evidence_ids for item in claim["evidence"]):
            raise ValueError(f"unresolved evidence: {claim['id']}")
        obj = claim.get("object")
        if isinstance(obj, dict) and obj.get("type") == "EntityReference" and obj.get("id") not in entity_ids:
            raise ValueError(f"unresolved object: {claim['id']}")
    for item in evidence:
        if item["source"] not in source_ids:
            raise ValueError(f"unresolved evidence source: {item['id']}")

    checksum_doc = load(migration / "checksums.json")
    for relative, expected_hash in checksum_doc["files"].items():
        actual_hash = hashlib.sha256((migration / relative).read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            raise ValueError(f"checksum mismatch: {relative}")
    if report["databaseSha256"] != hashlib.sha256(database.read_bytes()).hexdigest():
        raise ValueError("database hash mismatch")

    return {"status": "PASS", "counts": actual, "references": "resolved", "checksums": len(checksum_doc["files"])}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", type=Path, default=DEFAULT_DB)
    parser.add_argument("--migration", type=Path, default=DEFAULT_MIGRATION)
    args = parser.parse_args()
    print(json.dumps(validate(args.database.resolve(), args.migration.resolve()), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
