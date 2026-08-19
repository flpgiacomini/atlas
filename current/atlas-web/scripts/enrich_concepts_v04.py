#!/usr/bin/env python3
"""Publish the Alfa Romeo BAT 5, BAT 7 and BAT 9 aerodynamic lineage."""
import json,sqlite3
from pathlib import Path
from enrich_people_batch_01 import stable_uuid7
ROOT=Path(__file__).resolve().parents[1];DB=ROOT/'data'/'atlas.sqlite';NOW='2026-08-19T14:30:00+00:00'
URL='https://www.media.stellantis.com/es-es/alfa-romeo/press/70-anos-del-alfa-romeo-bat-7-el-concept-car-que-acabo-subastandose-en-sotheby-s'
ENTITIES={
'Alfa Romeo BAT 5':('vehicle','Primeiro automóvel concluído da série Berlinetta Aerodinamica Tecnica apresentada em 1953. Desenvolvido por Bertone e Franco Scaglione sobre a base técnica Alfa Romeo 1900, funcionou como investigação de baixa resistência aerodinâmica, integração formal da carroceria e possibilidades expressivas para um esportivo futuro.',{'vehicle_level':'standalone','vehicle_kind':'concept','editorial_batch':'V04'}),
'Alfa Romeo BAT 7':('vehicle','Segunda etapa publicada da série Berlinetta Aerodinamica Tecnica, apresentada em 1954. Bertone e Franco Scaglione aprofundaram a pesquisa aerodinâmica iniciada no BAT 5 sobre a plataforma Alfa Romeo 1900; a fonte institucional registra uso de fibra de vidro e coeficiente de arrasto excepcional para o período.',{'vehicle_level':'standalone','vehicle_kind':'concept','editorial_batch':'V04'}),
'Alfa Romeo BAT 9':('vehicle','Terceiro automóvel da sequência histórica BAT, apresentado em 1955. O projeto de Bertone e Franco Scaglione preservou a investigação aerodinâmica dos antecessores, mas aproximou alguns elementos da identidade visual Alfa Romeo, encerrando a trilogia como uma síntese entre experimento e reconhecimento de marca.',{'vehicle_level':'standalone','vehicle_kind':'concept','editorial_batch':'V04'}),
'Alfa Romeo':('brand','Marca italiana cuja base técnica Alfa Romeo 1900 sustentou os estudos BAT conduzidos com Bertone e Franco Scaglione. No Atlas, a marca conecta automóveis de passageiros, competição, pesquisa aerodinâmica e sucessivas colaborações com carrozzerie e designers independentes.',{'brand_status':'active','editorial_batch':'V04'}),
'Bertone':('organization','Carrozzeria e organização italiana de design responsável pelo desenvolvimento da série BAT em colaboração com Alfa Romeo e Franco Scaglione. O programa transformou pesquisa aerodinâmica, novos materiais e construção de protótipos em três estudos públicos apresentados entre 1953 e 1955.',{'organization_type':'coachbuilder and design house','editorial_batch':'V04'}),
'Franco Scaglione':('person','Designer italiano associado pela Alfa Romeo e por Bertone à criação da série Berlinetta Aerodinamica Tecnica. Seu trabalho nos BAT 5, 7 e 9 explorou superfícies de baixa resistência, aletas e volumes integrados como instrumentos simultaneamente técnicos e expressivos.',{'roles':['automotive designer'],'editorial_batch':'V04'}),
'Alfa Romeo 1900':('vehicle','Automóvel de passageiros utilizado como base técnica dos protótipos BAT desenvolvidos por Bertone e Franco Scaglione. Sua presença no Atlas permite separar o veículo de produção da série de carrocerias experimentais que reutilizou sua arquitetura entre 1953 e 1955.',{'vehicle_level':'model','vehicle_kind':'production','editorial_batch':'V04'}),}
REL={name:[('designed_by','Franco Scaglione'),('developed_by','Bertone'),('marketed_under','Alfa Romeo'),('based_on','Alfa Romeo 1900')] for name in ('Alfa Romeo BAT 5','Alfa Romeo BAT 7','Alfa Romeo BAT 9')}
def eid(db,n):
 r=db.execute('select id from entity where canonical_name=?',(n,)).fetchone()
 if not r:raise ValueError(n)
 return r[0]
def main():
 db=sqlite3.connect(DB);db.execute('pragma foreign_keys=on')
 try:
  for n,(t,d,m) in ENTITIES.items():db.execute('''insert into entity(id,entity_type,canonical_name,slug,description,metadata_json,created_at,updated_at) values(?,?,?,null,?,?,?,?) on conflict(id) do update set description=excluded.description,metadata_json=excluded.metadata_json,updated_at=excluded.updated_at''',(stable_uuid7('entity:'+n),t,n,d,json.dumps(m,ensure_ascii=False,sort_keys=True),NOW,NOW))
  src=stable_uuid7('source:'+URL);db.execute('''insert or ignore into source(id,source_type,title,publisher,published_at,url,accessed_at,language,source_tier,external_ids_json,notes,created_at,updated_at) values(?,'manufacturer_archive','70 años del Alfa Romeo BAT 7','Alfa Romeo / Stellantis','2024-07-24',?,'2026-08-19','es','A','{}','História institucional do programa BAT 5, 7 e 9.',?,?)''',(src,URL,NOW,NOW))
  for subject,rels in REL.items():
   sids=[]
   for pred,obj in rels:
    seed=f'{subject}:{pred}:{obj}:V04';sid=stable_uuid7('statement:'+seed);sids.append(sid);pid=db.execute('select id from predicate where name=?',(pred,)).fetchone()[0]
    db.execute('''insert or ignore into statement(id,subject_entity_id,predicate_id,object_type,object_entity_id,qualifiers_json,confidence,resolution_status,created_at,updated_at) values(?,?,?,'entity',?,?,'high','accepted',?,?)''',(sid,eid(db,subject),pid,eid(db,obj),json.dumps({'editorial_batch':'V04','program':'Berlinetta Aerodinamica Tecnica'}),NOW,NOW))
    cid=stable_uuid7('claim:'+seed);ev=stable_uuid7('evidence:'+seed)
    db.execute("insert or ignore into claim(id,statement_id,stance,support_strength,note,created_at) values(?,?,'supports','explicit','Relação documentada na história institucional da série BAT.',?)",(cid,sid,NOW))
    db.execute("insert or ignore into evidence(id,source_id,evidence_type,locator_json,notes,created_at) values(?,?,'manufacturer_history',?,'Matéria institucional Alfa Romeo/Stellantis sobre BAT 5, 7 e 9.',?)",(ev,src,json.dumps({'vehicle':subject,'predicate':pred},ensure_ascii=False),NOW))
    db.execute('insert or ignore into claim_evidence(claim_id,evidence_id) values(?,?)',(cid,ev))
   m=ENTITIES[subject][2]|{'description_basis_statement_ids':sids};db.execute('update entity set metadata_json=? where canonical_name=?',(json.dumps(m,ensure_ascii=False,sort_keys=True),subject))
  db.commit()
 except:db.rollback();raise
 finally:db.close()
 print(json.dumps({'published':list(REL),'support_entities':4,'relations':12},ensure_ascii=False))
if __name__=='__main__':main()
