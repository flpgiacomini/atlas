from pathlib import Path
from collections import defaultdict, deque
import sqlite3, json, shutil

ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/"data"/"atlas.sqlite"
GEN=ROOT/"src"/"data"/"generated"
PUBLIC=ROOT/"public"/"data"
GEN.mkdir(parents=True,exist_ok=True)
PUBLIC.mkdir(parents=True,exist_ok=True)

db=sqlite3.connect(DB)
db.row_factory=sqlite3.Row

GROUPS = {
    "genealogy": {"part_of","successor_of","derived_from","revival_of","inspired_by","based_on","configured_as","instance_of","shares_platform_with"},
    "industry": {"manufactured_by","produced_at","marketed_under","owned_by","subsidiary_of","operated_by","founded_by","developed_by"},
    "people": {"designed_by","engineered_by","invented_by","worked_at","led","collaborated_with"},
    "technology": {"uses_component","uses_technology","manufactured_using","introduced_by","popularized_by"},
    "geography": {"located_in","founded_in","layout_of","held_at","used_layout"},
    "motorsport": {"entry_for_event","entered_vehicle","entered_instance","entered_by","driven_by","part_of_season","season_of","governed_by"},
    "events": {"involved","resulted_in","affected","introduced_feature","restricted","required","prohibited"},
}
def relation_group(predicate):
    for group, names in GROUPS.items():
        if predicate in names:
            return group
    return "other"

def parse(value,default=None):
    if not value:return {} if default is None else default
    try:return json.loads(value)
    except:return {} if default is None else default

def literal(r):
    t=r["object_type"]
    if t=="entity":return r["object_name"]
    if t=="date":return r["object_date"]
    if t in ("number","quantity"):
        if r["object_number"] is None:return None
        unit=r["object_unit"] or ""
        return f"{r['object_number']:g}{(' '+unit) if unit else ''}"
    if t=="boolean":return bool(r["object_boolean"])
    return r["object_text"]

entities=[dict(r) for r in db.execute("SELECT * FROM entity ORDER BY canonical_name")]
by_id={e["id"]:e for e in entities}

sources_by_statement=defaultdict(list)
for r in db.execute("""
SELECT c.statement_id,c.stance,c.support_strength,
       e.locator_json,e.excerpt,
       src.id source_id,src.title,src.publisher,src.published_at,src.url,src.source_type,src.source_tier
FROM claim c
JOIN claim_evidence ce ON ce.claim_id=c.id
JOIN evidence e ON e.id=ce.evidence_id
JOIN source src ON src.id=e.source_id
ORDER BY src.publisher,src.title
"""):
    x=dict(r);x["locator"]=parse(x.pop("locator_json"),{})
    sources_by_statement[x.pop("statement_id")].append(x)

outgoing=defaultdict(list);incoming=defaultdict(list);edges=[];adj=defaultdict(list)
for r in db.execute("""
SELECT s.*,p.name predicate,
       se.canonical_name subject_name,se.entity_type subject_type,
       oe.canonical_name object_name,oe.entity_type object_entity_type
FROM statement s
JOIN predicate p ON p.id=s.predicate_id
JOIN entity se ON se.id=s.subject_entity_id
LEFT JOIN entity oe ON oe.id=s.object_entity_id
ORDER BY p.name
"""):
    x=dict(r)
    x["qualifiers"]=parse(x.pop("qualifiers_json"),{})
    x["sources"]=sources_by_statement.get(x["id"],[])
    x["value"]=literal(r)
    x["group"]=relation_group(x["predicate"])
    outgoing[x["subject_entity_id"]].append(x)
    if x["object_type"]=="entity":
        incoming[x["object_entity_id"]].append(x)
        edge={"id":x["id"],"s":x["subject_entity_id"],"p":x["predicate"],"o":x["object_entity_id"]}
        edges.append(edge);adj[edge["s"]].append(edge);adj[edge["o"]].append(edge)

def graph_for(eid,depth=2,limit=90):
    seen={eid:0};q=deque([eid]);nodes={};eds={}
    while q and len(nodes)<limit:
        cur=q.popleft();d=seen[cur]
        e=by_id.get(cur)
        if e:nodes[cur]={"id":cur,"name":e["canonical_name"],"type":e["entity_type"]}
        if d>=depth:continue
        for edge in adj[cur]:
            eds[edge["id"]]=edge
            for nid in (edge["s"],edge["o"]):
                e2=by_id.get(nid)
                if e2:nodes[nid]={"id":nid,"name":e2["canonical_name"],"type":e2["entity_type"]}
                if nid not in seen and len(nodes)<limit:
                    seen[nid]=d+1;q.append(nid)
    return {"root":eid,"nodes":list(nodes.values()),"edges":list(eds.values())}

timeline_global=[]
event_date={}
for r in db.execute("""
SELECT e.id,e.canonical_name,s.object_date,s.object_date_precision
FROM entity e
JOIN statement s ON s.subject_entity_id=e.id
JOIN predicate p ON p.id=s.predicate_id
WHERE e.entity_type='event' AND p.name='occurred_on' AND s.object_type='date'
ORDER BY s.object_date
"""):
    event_date[r["id"]]={"id":r["id"],"name":r["canonical_name"],"date":r["object_date"],"precision":r["object_date_precision"]}
    timeline_global.append(event_date[r["id"]])

pages=[]
for e in entities:
    eid=e["id"]
    related_event_ids=set()
    for s in incoming[eid]:
        if by_id.get(s["subject_entity_id"],{}).get("entity_type")=="event" and s["predicate"]=="involved":
            related_event_ids.add(s["subject_entity_id"])
    events=[event_date[x] for x in related_event_ids if x in event_date]
    events.sort(key=lambda x:x["date"])
    pages.append({
      "id":eid,
      "type":e["entity_type"],
      "name":e["canonical_name"],
      "description":e["description"],
      "metadata":parse(e["metadata_json"],{}),
      "names":[dict(r) for r in db.execute("SELECT value,name_type,language,valid_from,valid_until FROM entity_name WHERE entity_id=? ORDER BY name_type,value",(eid,))],
      "external_ids":[dict(r) for r in db.execute("SELECT scheme,value,url FROM external_identifier WHERE entity_id=? ORDER BY scheme,value",(eid,))],
      "outgoing":outgoing[eid],
      "incoming":incoming[eid],
      "events":events,
      "graph":graph_for(eid)
    })

(GEN/"entity-pages.json").write_text(json.dumps(pages,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
(GEN/"stats.json").write_text(json.dumps({
  "entities":len(entities),
  "statements":db.execute("SELECT COUNT(*) FROM statement").fetchone()[0],
  "sources":db.execute("SELECT COUNT(*) FROM source").fetchone()[0],
  "events":sum(1 for e in entities if e["entity_type"]=="event")
},ensure_ascii=False),encoding="utf-8")
(PUBLIC/"graph-index.json").write_text(json.dumps({
  "nodes":[{"id":e["id"],"name":e["canonical_name"],"type":e["entity_type"]} for e in entities],
  "edges":edges
},ensure_ascii=False,separators=(",",":")),encoding="utf-8")
(PUBLIC/"timeline.json").write_text(json.dumps(timeline_global,ensure_ascii=False,separators=(",",":")),encoding="utf-8")

compare_index=[]
for page in pages:
    scalar=[{
      "predicate":s["predicate"],"value":s["value"],"confidence":s["confidence"],"status":s["resolution_status"]
    } for s in page["outgoing"] if s["object_type"]!="entity"]
    links=[{
      "predicate":s["predicate"],"name":s["object_name"],"id":s["object_entity_id"]
    } for s in page["outgoing"] if s["object_type"]=="entity"]
    compare_index.append({
      "id":page["id"],"name":page["name"],"type":page["type"],
      "metadata":page["metadata"],"facts":scalar[:30],"links":links[:40]
    })
(PUBLIC/"compare-index.json").write_text(json.dumps(compare_index,ensure_ascii=False,separators=(",",":")),encoding="utf-8")

geo_registry=ROOT/"data"/"geography.registry.json"
if geo_registry.exists():
    shutil.copy2(geo_registry,PUBLIC/"geography.registry.json")

prototype=ROOT/"data"/"map-points.prototype.json"
if prototype.exists():
    shutil.copy2(prototype,PUBLIC/"map-points.prototype.json")

print(json.dumps({"pages":len(pages),"edges":len(edges),"timeline":len(timeline_global)},ensure_ascii=False))
db.close()
