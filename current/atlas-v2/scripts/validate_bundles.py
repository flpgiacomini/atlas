"""Validate Atlas v2 publication bundle coverage, hashes and journeys."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLES = ROOT / "bundles"
EXPECTED_PERIODS = {"1769-1885", "1886-1918", "1919-1939", "1940-1959", "1960-1979", "1980-1999", "2000-2009", "2010-2019", "2020-2026", "undated"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(root: Path) -> dict:
    manifest = load(root / "manifest.json")
    index = load(root / "index.json")
    journeys = load(root / "journeys.json")
    annual = load(root / "annual-chapters.json")
    if manifest["entityCount"] != index["count"] or index["count"] < 920:
        raise ValueError("entity index does not cover the migrated corpus")
    ids = [item["id"] for item in index["items"]]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate entity in index")
    for item in manifest["files"]:
        path = root / item["path"]
        if not path.is_file():
            raise ValueError(f"missing bundle: {item['path']}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
            raise ValueError(f"bundle checksum mismatch: {item['path']}")
        if load(path)["count"] != item["count"]:
            raise ValueError(f"bundle count mismatch: {item['path']}")
    period_keys = {item["key"] for item in manifest["files"] if item["kind"] == "period"}
    if period_keys != EXPECTED_PERIODS:
        raise ValueError(f"period coverage mismatch: {sorted(period_keys)}")
    if journeys["count"] != 6 or any(item["coverageState"] != "connected" for item in journeys["items"]):
        raise ValueError("six required journeys must be connected")
    annual_years = [item["year"] for item in annual["items"]]
    if annual["count"] < 117 or len(annual_years) != len(set(annual_years)):
        raise ValueError("annual chapters must be unique and cover the precursor anchors")
    if not set(range(1769, 1886)).issubset(annual_years):
        raise ValueError("annual chapters must fully cover 1769-1885")
    if any(item["coverageState"] != "authored" or not item.get("sources") for item in annual["items"]):
        raise ValueError("annual chapters must be authored and source-backed")
    return {
        "status": "PASS", "entities": index["count"], "bundles": len(manifest["files"]),
        "periods": len(period_keys), "journeys": journeys["count"],
        "annualChapters": annual["count"],
        "undated": next(item["count"] for item in manifest["files"] if item["kind"] == "period" and item["key"] == "undated"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundles", type=Path, default=DEFAULT_BUNDLES)
    args = parser.parse_args()
    print(json.dumps(validate(args.bundles.resolve()), sort_keys=True))


if __name__ == "__main__":
    main()
