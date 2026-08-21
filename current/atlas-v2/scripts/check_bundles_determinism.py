"""Build publication bundles twice and require byte-identical manifests."""

from __future__ import annotations

import hashlib
import json
import shutil

from build_bundles import ROOT, build


def digest(path):
    return hashlib.sha256((path / "manifest.json").read_bytes()).hexdigest()


def main() -> None:
    directory = ROOT / ".tmp-bundles"
    output = directory / "output"
    try:
        build(output)
        first = digest(output)
        build(output)
        second = digest(output)
        if first != second:
            raise ValueError(f"non-deterministic bundles: {first} != {second}")
    finally:
        if directory.exists():
            shutil.rmtree(directory)
    print(json.dumps({"status": "PASS", "manifestSha256": first, "runs": 2}, sort_keys=True))


if __name__ == "__main__":
    main()
