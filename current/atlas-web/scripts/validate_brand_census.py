#!/usr/bin/env python3
import csv,json,sqlite3,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; rows=list(csv.DictReader((ROOT/'data'/'brand.candidates.csv').open(encoding='utf-8-sig'))); errors=[]
names=Counter(r['candidate_name'].casefold() for r in rows); errors.extend(f'duplicate: {n}' for n,c in names.items() if c>1)
expected={f'M{i:02d}' for i in range(1,13)}; actual={r['wave'] for r in rows}
if actual!=expected: errors.append(f'waves: expected {sorted(expected)}, got {sorted(actual)}')
allowed={'published','needs_research','context_only','duplicate','out_of_scope'}
for i,row in enumerate(rows,2):
 if not row['candidate_name'].strip(): errors.append(f'row {i}: empty name')
 if row['decision'] not in allowed: errors.append(f"row {i}: invalid decision {row['decision']}")
 if row['decision']=='published' and not row['entity_id']: errors.append(f'row {i}: published without entity_id')
db=sqlite3.connect(ROOT/'data'/'atlas.sqlite')
brand_entities={r[0]:(r[1],r[2]) for r in db.execute("select id,canonical_name,entity_type from entity where entity_type='brand'")}
canonical={r[0].casefold() for r in brand_entities.values()}
db.close()
for i,row in enumerate(rows,2):
 if row['decision']!='published': continue
 entity=brand_entities.get(row['entity_id'])
 if not entity: errors.append(f'row {i}: published entity_id absent from SQLite brand entities')
 elif entity[0]!=row['candidate_name']: errors.append(f"row {i}: name mismatch CSV={row['candidate_name']!r} SQLite={entity[0]!r}")
missing=canonical-set(names)
errors.extend(f'published brand absent from census: {name}' for name in sorted(missing))
result={'passed':not errors,'errors':errors,'candidates':len(rows),'waves':len(actual),'decisions':dict(Counter(r['decision'] for r in rows))};print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(0 if not errors else 1)
