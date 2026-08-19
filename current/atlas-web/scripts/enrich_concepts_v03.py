#!/usr/bin/env python3
"""Publish GM Le Sabre and the Firebird I-III experimental lineage."""
import json, sqlite3
from pathlib import Path
from enrich_people_batch_01 import stable_uuid7
ROOT=Path(__file__).resolve().parents[1];DB=ROOT/'data'/'atlas.sqlite';NOW='2026-08-19T13:30:00+00:00'
SOURCES={
'Le Sabre':'https://news.gm.com/home.detail.html/Pages/topic/us/en/2026/may/0529-gm-invented-concept-car-changed-automotive-design.html',
'Firebird I':'https://www.gm.com/heritage/collection/gm-concept/1954-firebird-I',
'Firebird II':'https://www.gm.com/heritage/collection/gm-concept/1956-firebird-II',
'Firebird III':'https://www.gm.com/heritage/collection/gm-concept/1958-firebird-III'}
ENTITIES={
'General Motors Le Sabre':('vehicle','Concept car apresentado em 1951 como continuação da pesquisa iniciada pelo Buick Y-Job. Sob a liderança de Harley Earl e da organização de design da General Motors, sua forma inspirada em aviões a jato ajudou a estabelecer o repertório aeroespacial que dominaria os dream cars norte-americanos da década seguinte.',{'vehicle_level':'standalone','vehicle_kind':'concept','editorial_batch':'V03'}),
'General Motors Firebird I':('vehicle','Concept car experimental XP-21 de 1954, criado para investigar a viabilidade da turbina a gás em automóveis e explorar uma carroceria de plástico reforçado inspirada em aeronaves. A GM documenta testes reais, transmissão mecânica às rodas traseiras e refinamento aerodinâmico em túnel de vento do Caltech.',{'vehicle_level':'standalone','vehicle_kind':'concept','editorial_batch':'V03'}),
'General Motors Firebird II':('vehicle','Segundo automóvel experimental da série Firebird, apresentado no Motorama de 1956 como sucessor do Firebird I. Com quatro lugares, carroceria de titânio, turbina regenerativa e suspensão independente, também serviu de suporte narrativo para uma visão de rodovias eletronicamente guiadas.',{'vehicle_level':'standalone','vehicle_kind':'concept','editorial_batch':'V03'}),
'General Motors Firebird III':('vehicle','Terceiro concept car da linhagem Firebird, construído em 1958. A GM o identifica como o membro mais influente da série no desenho de veículos de produção, com soluções formais posteriormente refletidas em Cadillac de 1959 e 1961 e uma ruptura deliberada com convenções anteriores.',{'vehicle_level':'standalone','vehicle_kind':'concept','editorial_batch':'V03'}),
'Propulsão automotiva por turbina a gás':('technology','Aplicação experimental de turbinas a gás à propulsão de veículos rodoviários. A General Motors investigou essa alternativa durante décadas; os Firebird I, II e III materializaram diferentes estágios públicos do programa, sem que a solução alcançasse produção comercial de automóveis de passageiros.',{'technology_category':'propulsion','editorial_batch':'V03'}),
'Linguagem aeronáutica em concept cars':('technology','Estratégia de design que transpôs referências visuais e funcionais da aviação para automóveis experimentais do pós-guerra. Le Sabre e a série Firebird empregaram proporções, tomadas de ar, aletas, cabines e materiais para comunicar velocidade, pesquisa tecnológica e futuros possíveis.',{'technology_category':'design research','editorial_batch':'V03'}),}
REL={
'General Motors Le Sabre':[('designed_by','Harley Earl'),('developed_by','GM Design'),('successor_of','Buick Y-Job'),('uses_technology','Linguagem aeronáutica em concept cars')],
'General Motors Firebird I':[('designed_by','Harley Earl'),('developed_by','GM Design'),('successor_of','General Motors Le Sabre'),('uses_technology','Propulsão automotiva por turbina a gás')],
'General Motors Firebird II':[('developed_by','GM Design'),('successor_of','General Motors Firebird I'),('uses_technology','Propulsão automotiva por turbina a gás'),('uses_technology','Linguagem aeronáutica em concept cars')],
'General Motors Firebird III':[('developed_by','GM Design'),('successor_of','General Motors Firebird II'),('uses_technology','Propulsão automotiva por turbina a gás'),('uses_technology','Linguagem aeronáutica em concept cars')]}
def eid(db,n):
 r=db.execute('select id from entity where canonical_name=?',(n,)).fetchone()
 if not r: raise ValueError(n)
 return r[0]
def main():
 db=sqlite3.connect(DB);db.execute('pragma foreign_keys=on')
 try:
  for n,(t,d,m) in ENTITIES.items():db.execute('''insert into entity(id,entity_type,canonical_name,slug,description,metadata_json,created_at,updated_at) values(?,?,?,null,?,?,?,?) on conflict(id) do update set description=excluded.description,metadata_json=excluded.metadata_json,updated_at=excluded.updated_at''',(stable_uuid7('entity:'+n),t,n,d,json.dumps(m,ensure_ascii=False,sort_keys=True),NOW,NOW))
  src={}
  for key,url in SOURCES.items():
   src[key]=stable_uuid7('source:'+url);db.execute('''insert or ignore into source(id,source_type,title,publisher,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at) values(?,'manufacturer_archive',?,'General Motors',?,'2026-08-19','en','A','{}','Registro institucional GM Heritage/GM News.',?,?)''',(src[key],key,url,NOW,NOW))
  for subject,relations in REL.items():
   key='Le Sabre' if subject.endswith('Le Sabre') else subject.removeprefix('General Motors ');sids=[]
   for pred,obj in relations:
    seed=f'{subject}:{pred}:{obj}:V03';sid=stable_uuid7('statement:'+seed);sids.append(sid);pid=db.execute('select id from predicate where name=?',(pred,)).fetchone()[0]
    db.execute('''insert or ignore into statement(id,subject_entity_id,predicate_id,object_type,object_entity_id,qualifiers_json,confidence,resolution_status,created_at,updated_at) values(?,?,?,'entity',?,?,'high','accepted',?,?)''',(sid,eid(db,subject),pid,eid(db,obj),json.dumps({'editorial_batch':'V03','source_record':key}),NOW,NOW))
    cid=stable_uuid7('claim:'+seed);ev=stable_uuid7('evidence:'+seed)
    db.execute("insert or ignore into claim(id,statement_id,stance,support_strength,note,created_at) values(?,?,'supports','strong','Relação sustentada pela narrativa institucional do programa.',?)",(cid,sid,NOW))
    db.execute("insert or ignore into evidence(id,source_id,evidence_type,locator_json,notes,created_at) values(?,?,'collection_record',?,'Registro institucional do veículo e de sua linhagem.',?)",(ev,src[key],json.dumps({'vehicle':subject,'predicate':pred}),NOW))
    db.execute('insert or ignore into claim_evidence(claim_id,evidence_id) values(?,?)',(cid,ev))
   m=ENTITIES[subject][2]|{'description_basis_statement_ids':sids};db.execute('update entity set metadata_json=? where canonical_name=?',(json.dumps(m,ensure_ascii=False,sort_keys=True),subject))
  db.commit()
 except:db.rollback();raise
 finally:db.close()
 print(json.dumps({'published':list(REL),'support_entities':2,'relations':sum(map(len,REL.values()))},ensure_ascii=False))
if __name__=='__main__':main()
