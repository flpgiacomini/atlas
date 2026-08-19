from pathlib import Path
import csv
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
        expected = {"entity":384,"statement":591,"source":154,"claim":717,"evidence":718,"predicate":56}
        actual = {table: db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] for table in expected}
        db.close(); self.assertEqual(actual, expected)

    def test_every_entity_has_media(self):
        db = sqlite3.connect(ROOT / "data" / "atlas.sqlite")
        entity_count = db.execute("SELECT COUNT(*) FROM entity").fetchone()[0]
        db.close()
        manifest = json.loads((ROOT / "data" / "media.manifest.json").read_text(encoding="utf-8"))
        ids = [item["entity_id"] for item in manifest["items"]]
        self.assertEqual(len(ids), entity_count); self.assertEqual(len(set(ids)), entity_count)

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
        db = sqlite3.connect(ROOT / "data" / "atlas.sqlite")
        entity_count = db.execute("SELECT COUNT(*) FROM entity").fetchone()[0]
        db.close()
        self.assertEqual(summary["entities"], entity_count)
        self.assertEqual(summary["statuses"].get("stub", 0), 0)
        self.assertEqual(summary["statuses"].get("partial", 0), 0)

    def test_every_entity_has_editorial_narrative_and_batch(self):
        db = sqlite3.connect(ROOT / "data" / "atlas.sqlite")
        rows = db.execute("SELECT description, metadata_json FROM entity").fetchall()
        db.close()
        self.assertGreaterEqual(len(rows), 366)
        self.assertTrue(all(len((description or "").split()) >= 30 for description, _ in rows))
        self.assertTrue(all(json.loads(metadata).get("editorial_batch") for _, metadata in rows))

    def test_brand_history_projection_has_vehicle_coverage(self):
        pages = json.loads((ROOT / "src" / "data" / "generated" / "entity-pages.json").read_text(encoding="utf-8"))
        brands = [page for page in pages if page["type"] == "brand"]
        db = sqlite3.connect(ROOT / "data" / "atlas.sqlite")
        brand_count = db.execute("SELECT COUNT(*) FROM entity WHERE entity_type='brand'").fetchone()[0]
        db.close()
        self.assertEqual(len(brands), brand_count)
        for brand in brands:
            vehicles = [page for page in pages if page["type"] == "vehicle" and any(
                relation["predicate"] == "marketed_under" and relation["object_entity_id"] == brand["id"]
                for relation in page["outgoing"]
            )]
            self.assertGreater(len(vehicles), 0, brand["name"])

    def test_published_candidate_registries_resolve_to_sqlite(self):
        for validator in ("validate_brand_census.py", "validate_historical_significance.py"):
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / validator)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_all_remaining_historical_candidates_are_editorially_validated(self):
        ledger = json.loads((ROOT / "data" / "historical-significance.validation.json").read_text(encoding="utf-8"))
        self.assertEqual(ledger["summary"]["total"], 54)
        with (ROOT / "data" / "historical-significance.candidates.csv").open(encoding="utf-8") as stream:
            candidates = list(csv.DictReader(stream))
        self.assertEqual(ledger["summary"]["remaining_candidates_validated"], sum(row["decision"] == "include_candidate" for row in candidates))
        self.assertEqual(ledger["summary"]["failed"], 0)
        remaining = [record for record in ledger["records"] if record["validation_status"] == "validated_for_research"]
        self.assertTrue(all(record["relevance_passed"] for record in remaining))
        self.assertTrue(all(record["source_gate"] == "required_before_publication" for record in remaining))

if __name__ == "__main__": unittest.main()
