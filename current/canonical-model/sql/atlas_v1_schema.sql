
PRAGMA foreign_keys=ON;

CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);

CREATE TABLE entity(
 id TEXT PRIMARY KEY, entity_type TEXT NOT NULL, canonical_name TEXT NOT NULL, slug TEXT,
 description TEXT, metadata_json TEXT NOT NULL DEFAULT '{}', created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
 CHECK(length(id)=36)
);
CREATE UNIQUE INDEX ux_entity_slug ON entity(slug) WHERE slug IS NOT NULL;
CREATE INDEX ix_entity_type ON entity(entity_type);
CREATE INDEX ix_entity_name ON entity(canonical_name);

CREATE TABLE entity_name(
 id TEXT PRIMARY KEY, entity_id TEXT NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
 value TEXT NOT NULL, name_type TEXT NOT NULL, language TEXT,
 valid_from TEXT, valid_from_precision TEXT, valid_until TEXT, valid_until_precision TEXT,
 source_note TEXT, created_at TEXT NOT NULL
);

CREATE TABLE external_identifier(
 id TEXT PRIMARY KEY, entity_id TEXT NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
 scheme TEXT NOT NULL, value TEXT NOT NULL, url TEXT, created_at TEXT NOT NULL,
 UNIQUE(entity_id,scheme,value)
);
CREATE INDEX ix_external_identifier_lookup ON external_identifier(scheme,value);

CREATE TABLE legacy_identifier(
 legacy_id TEXT PRIMARY KEY, canonical_id TEXT NOT NULL, object_kind TEXT NOT NULL,
 source_dataset TEXT, migrated_at TEXT NOT NULL
);

CREATE TABLE predicate(
 id TEXT PRIMARY KEY, name TEXT NOT NULL UNIQUE, description TEXT NOT NULL,
 subject_types_json TEXT NOT NULL, object_types_json TEXT NOT NULL,
 temporal_policy TEXT NOT NULL, symmetric INTEGER NOT NULL DEFAULT 0 CHECK(symmetric IN(0,1)),
 status TEXT NOT NULL DEFAULT 'active', created_at TEXT NOT NULL
);

CREATE TABLE statement(
 id TEXT PRIMARY KEY,
 subject_entity_id TEXT NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
 predicate_id TEXT NOT NULL REFERENCES predicate(id),
 object_type TEXT NOT NULL CHECK(object_type IN('entity','string','date','number','quantity','boolean')),
 object_entity_id TEXT REFERENCES entity(id),
 object_text TEXT, object_number REAL, object_unit TEXT, object_date TEXT, object_date_precision TEXT,
 object_boolean INTEGER CHECK(object_boolean IS NULL OR object_boolean IN(0,1)),
 valid_from TEXT, valid_from_precision TEXT, valid_until TEXT, valid_until_precision TEXT,
 qualifiers_json TEXT NOT NULL DEFAULT '{}',
 confidence TEXT NOT NULL CHECK(confidence IN('high','medium','low','disputed','unknown')),
 resolution_status TEXT NOT NULL CHECK(resolution_status IN('accepted','disputed','unresolved','needs_reconciliation','rejected')),
 created_at TEXT NOT NULL, updated_at TEXT NOT NULL, CHECK(length(id)=36),
 CHECK(
  (object_type='entity' AND object_entity_id IS NOT NULL AND object_text IS NULL AND object_number IS NULL AND object_date IS NULL AND object_boolean IS NULL)
 OR (object_type='string' AND object_text IS NOT NULL AND object_entity_id IS NULL AND object_number IS NULL AND object_date IS NULL AND object_boolean IS NULL)
 OR (object_type='date' AND object_date IS NOT NULL AND object_entity_id IS NULL AND object_text IS NULL AND object_number IS NULL AND object_boolean IS NULL)
 OR (object_type='number' AND object_number IS NOT NULL AND object_entity_id IS NULL AND object_text IS NULL AND object_date IS NULL AND object_boolean IS NULL)
 OR (object_type='quantity' AND object_number IS NOT NULL AND object_unit IS NOT NULL AND object_entity_id IS NULL AND object_text IS NULL AND object_date IS NULL AND object_boolean IS NULL)
 OR (object_type='boolean' AND object_boolean IS NOT NULL AND object_entity_id IS NULL AND object_text IS NULL AND object_number IS NULL AND object_date IS NULL)
 )
);
CREATE INDEX ix_statement_subject ON statement(subject_entity_id);
CREATE INDEX ix_statement_predicate ON statement(predicate_id);
CREATE INDEX ix_statement_object_entity ON statement(object_entity_id);

CREATE TABLE source(
 id TEXT PRIMARY KEY, source_type TEXT NOT NULL, title TEXT NOT NULL, author TEXT, publisher TEXT,
 published_at TEXT, url TEXT, accessed_at TEXT, language TEXT, source_tier TEXT, zotero_key TEXT,
 external_ids_json TEXT NOT NULL DEFAULT '{}', notes TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
 CHECK(length(id)=36)
);

CREATE TABLE claim(
 id TEXT PRIMARY KEY, statement_id TEXT NOT NULL REFERENCES statement(id) ON DELETE CASCADE,
 stance TEXT NOT NULL CHECK(stance IN('supports','contradicts','qualifies','mentions')),
 support_strength TEXT NOT NULL CHECK(support_strength IN('explicit','strong','indirect','weak')),
 note TEXT, created_at TEXT NOT NULL, CHECK(length(id)=36)
);

CREATE TABLE evidence(
 id TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES source(id) ON DELETE CASCADE,
 evidence_type TEXT NOT NULL, locator_json TEXT NOT NULL DEFAULT '{}', excerpt TEXT, notes TEXT,
 created_at TEXT NOT NULL, CHECK(length(id)=36)
);

CREATE TABLE claim_evidence(
 claim_id TEXT NOT NULL REFERENCES claim(id) ON DELETE CASCADE,
 evidence_id TEXT NOT NULL REFERENCES evidence(id) ON DELETE CASCADE,
 PRIMARY KEY(claim_id,evidence_id)
);

CREATE TABLE entity_redirect(
 old_entity_id TEXT PRIMARY KEY,
 canonical_entity_id TEXT NOT NULL REFERENCES entity(id),
 reason TEXT NOT NULL, created_at TEXT NOT NULL
);

CREATE VIEW v_entity_edge AS
SELECT s.id statement_id,se.id subject_id,se.canonical_name subject_name,p.name predicate,
       oe.id object_id,oe.canonical_name object_name,s.valid_from,s.valid_until,
       s.confidence,s.resolution_status,s.qualifiers_json
FROM statement s
JOIN entity se ON se.id=s.subject_entity_id
JOIN predicate p ON p.id=s.predicate_id
JOIN entity oe ON oe.id=s.object_entity_id
WHERE s.object_type='entity';

CREATE VIEW v_statement_source AS
SELECT s.id statement_id,se.canonical_name subject_name,p.name predicate,
 CASE s.object_type
  WHEN 'entity' THEN oe.canonical_name
  WHEN 'date' THEN s.object_date
  WHEN 'number' THEN CAST(s.object_number AS TEXT)
  WHEN 'quantity' THEN CAST(s.object_number AS TEXT)||' '||s.object_unit
  WHEN 'boolean' THEN CASE s.object_boolean WHEN 1 THEN 'true' ELSE 'false' END
  ELSE s.object_text END object_value,
 c.stance,c.support_strength,src.title source_title,src.publisher,src.url,e.locator_json
FROM statement s
JOIN entity se ON se.id=s.subject_entity_id
JOIN predicate p ON p.id=s.predicate_id
LEFT JOIN entity oe ON oe.id=s.object_entity_id
LEFT JOIN claim c ON c.statement_id=s.id
LEFT JOIN claim_evidence ce ON ce.claim_id=c.id
LEFT JOIN evidence e ON e.id=ce.evidence_id
LEFT JOIN source src ON src.id=e.source_id;
