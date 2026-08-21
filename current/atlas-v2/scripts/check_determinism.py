"""Generate the v2 migration twice and require byte-identical manifests."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from migrate_sqlite import DEFAULT_DB, ROOT, migrate


def manifest_hash(path: Path) -> str:
    return hashlib.sha256((path / "checksums.json").read_bytes()).hexdigest()


def main() -> None:
    directory = ROOT / ".tmp-determinism"
    output = directory / "migration"
    try:
        migrate(DEFAULT_DB, output)
        first = manifest_hash(output)
        migrate(DEFAULT_DB, output)
        second = manifest_hash(output)
        if first != second:
            raise ValueError(f"non-deterministic migration: {first} != {second}")
    finally:
        if directory.exists():
            shutil.rmtree(directory)
    print(json.dumps({"status": "PASS", "manifestSha256": first, "runs": 2}, sort_keys=True))


if __name__ == "__main__":
    main()
