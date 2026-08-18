from pathlib import Path
import json
import sqlite3
import unittest
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

class AtlasContracts(unittest.TestCase):
    def test_unfinished_heurist_gate_is_not_approved(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_heurist_report.py")],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('"status": "in_progress"', result.stdout)
    def test_canonical_counts(self):
        db = sqlite3.connect(ROOT / "data" / "atlas.sqlite")
        expected = {"entity":339,"statement":446,"source":125,"claim":572,"evidence":572,"predicate":54}
        actual = {table: db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] for table in expected}
        db.close(); self.assertEqual(actual, expected)

    def test_every_entity_has_media(self):
        manifest = json.loads((ROOT / "data" / "media.manifest.json").read_text(encoding="utf-8"))
        ids = [item["entity_id"] for item in manifest["items"]]
        self.assertEqual(len(ids), 339); self.assertEqual(len(set(ids)), 339)

    def test_geography_is_release_ready(self):
        rows = json.loads((ROOT / "data" / "geography.registry.json").read_text(encoding="utf-8"))
        self.assertEqual(len(rows), 4); self.assertTrue(all(row["release_ready"] for row in rows))

    def test_no_prototype_map(self):
        self.assertFalse((ROOT / "data" / "map-points.prototype.json").exists())

if __name__ == "__main__": unittest.main()
