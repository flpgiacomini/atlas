#!/usr/bin/env python3
import csv,json,sqlite3,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'historical-significance.candidates.csv';rows=list(csv.DictReader(path.open(encoding='utf-8')));errors=[]
ledger_path=ROOT/'data'/'historical-significance.validation.json'
allowed_kinds={'concept','prototype','prototype_program','one_off'};allowed_decisions={'published','include_candidate','context_only','hold','exclude'};tracks={'TEC','IND','DES','SEG','ESP','SOC','GEO','GEN'}
names=Counter(r['candidate_name'].casefold() for r in rows);errors.extend(f'duplicate: {n}' for n,c in names.items() if c>1)
for line,row in enumerate(rows,2):
 if row['kind'] not in allowed_kinds: errors.append(f"row {line}: invalid kind {row['kind']}")
 if row['decision'] not in allowed_decisions: errors.append(f"row {line}: invalid decision {row['decision']}")
 if row['decision']=='published' and not (row.get('entity_id') or '').strip(): errors.append(f'row {line}: published without entity_id')
 unknown=set(row['contribution_tracks'].split('|'))-tracks
 if unknown: errors.append(f'row {line}: unknown tracks {sorted(unknown)}')
 if len(row['rationale'].split())<6: errors.append(f'row {line}: rationale too short')
db=sqlite3.connect(ROOT/'data'/'atlas.sqlite')
entities={row[0]:(row[1],row[2]) for row in db.execute('select id,canonical_name,entity_type from entity')}
db.close()
for line,row in enumerate(rows,2):
 if row['decision']!='published': continue
 entity=entities.get((row.get('entity_id') or '').strip())
 if not entity: errors.append(f'row {line}: published entity_id absent from SQLite')
 elif entity[0]!=row['candidate_name']: errors.append(f"row {line}: name mismatch CSV={row['candidate_name']!r} SQLite={entity[0]!r}")
 elif entity[1]!='vehicle': errors.append(f'row {line}: published candidate must resolve to vehicle, got {entity[1]}')
if not ledger_path.exists(): errors.append('validation ledger missing')
else:
 ledger=json.loads(ledger_path.read_text(encoding='utf-8'))
 ledger_names={r['candidate_name'] for r in ledger.get('records',[])}
 csv_names={r['candidate_name'] for r in rows}
 if ledger_names!=csv_names: errors.append('validation ledger candidates differ from CSV')
 if ledger.get('summary',{}).get('failed')!=0: errors.append('validation ledger contains failed candidates')
 expected_remaining=sum(r['decision']=='include_candidate' for r in rows)
 if ledger.get('summary',{}).get('remaining_candidates_validated')!=expected_remaining: errors.append(f'expected {expected_remaining} remaining validated candidates')
result={'passed':not errors,'errors':errors,'candidates':len(rows),'kinds':dict(Counter(r['kind'] for r in rows)),'decisions':dict(Counter(r['decision'] for r in rows))};print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(0 if not errors else 1)
