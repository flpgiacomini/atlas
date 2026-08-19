#!/usr/bin/env python3
"""Publish the first validated concept-car record: the 1938 Buick Y-Job."""
import json, sqlite3
from pathlib import Path
from enrich_people_batch_01 import stable_uuid7
ROOT=Path(__file__).resolve().parents[1]; DB=ROOT/'data'/'atlas.sqlite'; NOW='2026-08-19T12:30:00+00:00'
URL='https://www.gm.com/heritage/collection/buick/1938-buick-y-job-concept'
ENTITIES={
'Buick Y-Job':('vehicle','Concept car construído em 1938 para explorar antecipadamente forma, equipamentos e reação pública, sem intenção imediata de produção. Concebido por Harley Earl e pela organização hoje conhecida como GM Design, usou chassi Buick de 1937 e antecipou faróis ocultos, maçanetas niveladas, capota recolhida sob cobertura metálica e vidros elétricos.',{'vehicle_level':'standalone','vehicle_kind':'concept','editorial_batch':'V02'}),
'Buick':('brand','Marca automotiva norte-americana sob a qual o Y-Job de 1938 foi apresentado. No Atlas, sua história será conectada à estrutura industrial da General Motors, aos automóveis de passageiros e ao papel pioneiro do Y-Job na institucionalização do concept car.',{'brand_status':'active','editorial_batch':'V02'}),
'Harley Earl':('person','Designer norte-americano que liderou a criação do Buick Y-Job e a formação da prática de design avançado na General Motors. O registro institucional da GM atribui a ele a concepção do veículo como referência para projetos futuros e laboratório móvel de soluções.',{'roles':['designer','design executive'],'editorial_batch':'V02'}),
'GM Design':('organization','Organização de design da General Motors à qual a fonte institucional atribui o desenvolvimento do Buick Y-Job sob liderança de Harley Earl. Sua atuação ajudou a transformar o concept car em instrumento sistemático de pesquisa, comunicação pública e antecipação de linguagem automotiva.',{'organization_type':'design organization','editorial_batch':'V02'}),
'Faróis retráteis':('technology','Solução de iluminação na qual os faróis permanecem ocultos ou nivelados quando não utilizados. O Buick Y-Job empregou faróis escondidos como parte de sua pesquisa formal; a solução mais tarde apareceu em automóveis produzidos em série por diferentes fabricantes.',{'technology_category':'lighting and body integration','editorial_batch':'V02'}),}
REL=[('designed_by','Harley Earl'),('developed_by','GM Design'),('marketed_under','Buick'),('uses_technology','Faróis retráteis')]
def eid(db,n):
 r=db.execute('select id from entity where canonical_name=?',(n,)).fetchone()
 if not r: raise ValueError(n)
 return r[0]
def main():
 db=sqlite3.connect(DB);db.execute('pragma foreign_keys=on')
 try:
  for n,(t,d,m) in ENTITIES.items(): db.execute('''insert into entity(id,entity_type,canonical_name,slug,description,metadata_json,created_at,updated_at) values(?,?,?,null,?,?,?,?) on conflict(id) do update set description=excluded.description,metadata_json=excluded.metadata_json,updated_at=excluded.updated_at''',(stable_uuid7('entity:'+n),t,n,d,json.dumps(m,ensure_ascii=False,sort_keys=True),NOW,NOW))
  src=stable_uuid7('source:'+URL);db.execute('''insert or ignore into source(id,source_type,title,publisher,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at) values(?,'manufacturer_archive','1938 Buick Y-Job Concept','General Motors',?,'2026-08-19','en','A','{}','Registro da GM Heritage Collection.',?,?)''',(src,URL,NOW,NOW))
  sids=[]
  for pred,obj in REL:
   seed=f'Buick Y-Job:{pred}:{obj}:gm-heritage';sid=stable_uuid7('statement:'+seed);sids.append(sid);pid=db.execute('select id from predicate where name=?',(pred,)).fetchone()[0]
   db.execute('''insert or ignore into statement(id,subject_entity_id,predicate_id,object_type,object_entity_id,qualifiers_json,confidence,resolution_status,created_at,updated_at) values(?,?,?,'entity',?,'{"editorial_batch":"V02"}','high','accepted',?,?)''',(sid,eid(db,'Buick Y-Job'),pid,eid(db,obj),NOW,NOW))
   cid=stable_uuid7('claim:'+seed);ev=stable_uuid7('evidence:'+seed)
   db.execute("insert or ignore into claim(id,statement_id,stance,support_strength,note,created_at) values(?,?,'supports','explicit','Relação explicitada pela coleção histórica da fabricante.',?)",(cid,sid,NOW))
   db.execute("insert or ignore into evidence(id,source_id,evidence_type,locator_json,notes,created_at) values(?,?,'collection_record',?,'Página individual do veículo; sem reprodução extensa.',?)",(ev,src,json.dumps({'vehicle':'1938 Buick Y-Job Concept','relation':pred}),NOW))
   db.execute('insert or ignore into claim_evidence(claim_id,evidence_id) values(?,?)',(cid,ev))
  m=ENTITIES['Buick Y-Job'][2]|{'description_basis_statement_ids':sids};db.execute('update entity set metadata_json=? where canonical_name=?',(json.dumps(m,ensure_ascii=False,sort_keys=True),'Buick Y-Job'))
  db.commit()
 except: db.rollback();raise
 finally: db.close()
 print(json.dumps({'published':['Buick Y-Job'],'support_entities':4,'relations':4},ensure_ascii=False))
if __name__=='__main__': main()
