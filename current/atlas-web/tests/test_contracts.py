from pathlib import Path
import json
import sqlite3
import unittest
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

class AtlasContracts(unittest.TestCase):
    def test_completed_heurist_gate_is_approved(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_heurist_report.py")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertTrue(report["passed"])
        self.assertEqual(report["status"], "completed")
        self.assertEqual(report["score"], 9)
        self.assertFalse(report["critical_semantic_loss"])
    def test_canonical_counts(self):
        db = sqlite3.connect(ROOT / "data" / "atlas.sqlite")
        expected = {"entity":339,"statement":481,"source":139,"claim":607,"evidence":607,"predicate":56}
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

    def test_editorial_audit_covers_every_entity(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "audit_editorial_completeness.py")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["entities"], 339)
        self.assertEqual(summary["statuses"].get("stub", 0), 0)

    def test_every_entity_has_editorial_narrative_and_batch(self):
        db = sqlite3.connect(ROOT / "data" / "atlas.sqlite")
        rows = db.execute("SELECT description, metadata_json FROM entity").fetchall()
        db.close()
        self.assertEqual(len(rows), 339)
        self.assertTrue(all(len((description or "").split()) >= 30 for description, _ in rows))
        self.assertTrue(all(json.loads(metadata).get("editorial_batch") for _, metadata in rows))

if __name__ == "__main__": unittest.main()
