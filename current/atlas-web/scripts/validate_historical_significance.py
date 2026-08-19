#!/usr/bin/env python3
import csv,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'historical-significance.candidates.csv';rows=list(csv.DictReader(path.open(encoding='utf-8')));errors=[]
allowed_kinds={'concept','prototype','prototype_program','one_off'};allowed_decisions={'include_candidate','context_only','hold','exclude'};tracks={'TEC','IND','DES','SEG','ESP','SOC','GEO','GEN'}
names=Counter(r['candidate_name'].casefold() for r in rows);errors.extend(f'duplicate: {n}' for n,c in names.items() if c>1)
for line,row in enumerate(rows,2):
 if row['kind'] not in allowed_kinds: errors.append(f"row {line}: invalid kind {row['kind']}")
 if row['decision'] not in allowed_decisions: errors.append(f"row {line}: invalid decision {row['decision']}")
 unknown=set(row['contribution_tracks'].split('|'))-tracks
 if unknown: errors.append(f'row {line}: unknown tracks {sorted(unknown)}')
 if len(row['rationale'].split())<6: errors.append(f'row {line}: rationale too short')
result={'passed':not errors,'errors':errors,'candidates':len(rows),'kinds':dict(Counter(r['kind'] for r in rows)),'decisions':dict(Counter(r['decision'] for r in rows))};print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(0 if not errors else 1)
