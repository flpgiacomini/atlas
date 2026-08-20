#!/usr/bin/env python3
"""Generate the deterministic editorial-validation ledger for every candidate."""
from __future__ import annotations
import csv, json, sqlite3
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'data'/'historical-significance.candidates.csv'
OUTPUT=ROOT/'data'/'historical-significance.validation.json'
TRACKS={'TEC','IND','DES','SEG','ESP','SOC','GEO','GEN'}

def main():
 rows=list(csv.DictReader(INPUT.open(encoding='utf-8-sig')))
 db=sqlite3.connect(ROOT/'data'/'atlas.sqlite')
 canonical={r[0].casefold():r[1] for r in db.execute('select canonical_name,id from entity')}
 db.close()
 records=[]
 for row in rows:
  tracks=[value for value in row['contribution_tracks'].split('|') if value]
  checks={
   'identity_present':bool(row['candidate_name'].strip()),
   'year_valid':row['year'].isdigit() and 1886<=int(row['year'])<=2026,
   'kind_controlled':row['kind'] in {'concept','prototype','prototype_program','one_off'},
   'tracks_controlled':len(tracks)>=2 and not(set(tracks)-TRACKS),
   'rationale_substantive':len(row['rationale'].split())>=6,
   'not_unresolved_duplicate':row['decision'] in {'published','cataloged'} or row['candidate_name'].casefold() not in canonical,
  }
  relevance_passed=all(checks.values())
  if row['decision']=='published':
   status='published_validated';source_gate='satisfied'
  elif row['decision']=='cataloged':
   status='cataloged_attributed';source_gate='required_before_editorial_promotion'
  elif row['decision']=='include_candidate' and relevance_passed:
   status='validated_for_research';source_gate='required_before_publication'
  elif row['decision']=='context_only':
   status='validated_as_context';source_gate='required_if_promoted'
  elif row['decision']=='hold':
   status='validated_hold';source_gate='blocking'
  else:
   status='validation_failed';source_gate='blocking'
  records.append({
   'candidate_name':row['candidate_name'],'kind':row['kind'],'year':int(row['year']),
   'associated_brand':row['associated_brand'],'decision':row['decision'],
   'validation_status':status,'relevance_passed':relevance_passed,
   'checks':checks,'source_gate':source_gate,
   'validation_policy':'Registros catalográficos são pesquisáveis e atribuídos; fonte individual e relações evidenciadas são obrigatórias antes da promoção editorial.',
  })
 summary={'total':len(records),'statuses':dict(Counter(r['validation_status'] for r in records)),
          'remaining_candidates_validated':sum(r['validation_status']=='validated_for_research' for r in records),
          'failed':sum(r['validation_status']=='validation_failed' for r in records)}
 OUTPUT.write_text(json.dumps({'version':'1.0.0','validated_at':'2026-08-19','summary':summary,'records':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False))
 return 0 if not summary['failed'] else 1
if __name__=='__main__':raise SystemExit(main())
