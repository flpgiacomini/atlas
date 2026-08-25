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
        expected = {"entity":920,"statement":610,"source":202,"claim":736,"evidence":737,"predicate":56}
        actual = {table: db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] for table in expected}
        db.close(); self.assertEqual(actual, expected)

    def test_every_entity_has_media(self):
        db = sqlite3.connect(ROOT / "data" / "atlas.sqlite")
        required_count = db.execute("SELECT COUNT(*) FROM entity WHERE json_extract(metadata_json,'$.editorial_level')!='catalog'").fetchone()[0]
        db.close()
        manifest = json.loads((ROOT / "data" / "media.manifest.json").read_text(encoding="utf-8"))
        ids = [item["entity_id"] for item in manifest["items"]]
        self.assertEqual(len(ids), required_count); self.assertEqual(len(set(ids)), required_count)

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
        rows = db.execute("SELECT description, metadata_json FROM entity WHERE json_extract(metadata_json,'$.editorial_level')!='catalog'").fetchall()
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
        for brand in [item for item in brands if item["metadata"].get("editorial_level", "editorial") != "catalog"]:
            vehicles = [page for page in pages if page["type"] == "vehicle" and any(
                relation["predicate"] == "marketed_under" and relation["object_entity_id"] == brand["id"]
                for relation in page["outgoing"]
            )]
            self.assertGreater(len(vehicles), 0, brand["name"])

    def test_mass_catalog_is_attributed_and_separate_from_editorial_records(self):
        db = sqlite3.connect(ROOT / "data" / "atlas.sqlite")
        catalog_count = db.execute("SELECT COUNT(*) FROM entity WHERE json_extract(metadata_json,'$.editorial_level')='catalog'").fetchone()[0]
        attributed_count = db.execute("""SELECT COUNT(DISTINCT e.id) FROM entity e JOIN external_identifier x ON x.entity_id=e.id
            WHERE json_extract(e.metadata_json,'$.editorial_level')='catalog' AND x.scheme IN ('atlas-brand-census','atlas-significance-candidate')""").fetchone()[0]
        db.close()
        self.assertEqual(catalog_count, 522)
        self.assertEqual(attributed_count, catalog_count)

    def test_priority_catalog_has_source_backed_records(self):
        db = sqlite3.connect(ROOT / "data" / "atlas.sqlite")
        records = db.execute("""SELECT e.id,e.description,e.metadata_json,COUNT(DISTINCT src.id)
            FROM entity e JOIN statement s ON s.subject_entity_id=e.id
            JOIN claim c ON c.statement_id=s.id JOIN claim_evidence ce ON ce.claim_id=c.id
            JOIN evidence ev ON ev.id=ce.evidence_id JOIN source src ON src.id=ev.source_id
            WHERE json_extract(e.metadata_json,'$.verification_batch')='R01' GROUP BY e.id""").fetchall()
        db.close()
        self.assertEqual(len(records), 6)
        self.assertTrue(all(len(description.split()) >= 30 for _, description, _, _ in records))
        self.assertTrue(all(json.loads(metadata)["editorial_level"] == "catalog" for _, _, metadata, _ in records))
        self.assertTrue(all(source_count >= 1 for _, _, _, source_count in records))

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
        with (ROOT / "data" / "historical-significance.candidates.csv").open(encoding="utf-8-sig") as stream:
            candidates = list(csv.DictReader(stream))
        self.assertEqual(ledger["summary"]["remaining_candidates_validated"], sum(row["decision"] == "include_candidate" for row in candidates))
        self.assertEqual(ledger["summary"]["failed"], 0)
        remaining = [record for record in ledger["records"] if record["validation_status"] == "validated_for_research"]
        self.assertTrue(all(record["relevance_passed"] for record in remaining))
        self.assertTrue(all(record["source_gate"] == "required_before_publication" for record in remaining))

if __name__ == "__main__": unittest.main()
