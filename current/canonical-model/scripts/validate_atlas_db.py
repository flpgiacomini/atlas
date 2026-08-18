#!/usr/bin/env python3
import sqlite3, json, re, sys
UUID7=re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
db=sqlite3.connect(sys.argv[1]); db.row_factory=sqlite3.Row
errors=[]; warnings=[]
for t in ["entity","predicate","statement","source","claim","evidence"]:
    for r in db.execute(f"SELECT id FROM {t}"):
        if not UUID7.match(r["id"]): errors.append(f"{t}: invalid UUIDv7 {r['id']}")
for r in db.execute("PRAGMA foreign_key_check"): errors.append(f"foreign key violation: {tuple(r)}")
for r in db.execute("""SELECT c.id FROM claim c LEFT JOIN claim_evidence ce ON ce.claim_id=c.id WHERE ce.claim_id IS NULL"""):
    errors.append(f"claim without evidence: {r['id']}")
for r in db.execute("""SELECT lower(canonical_name) n,count(*) c FROM entity GROUP BY lower(canonical_name) HAVING c>1"""):
    warnings.append(f"reconcile canonical name: {r['n']} ({r['c']})")
print(json.dumps({"passed":not errors,"errors":errors,"warnings":warnings},ensure_ascii=False,indent=2))
raise SystemExit(0 if not errors else 1)
