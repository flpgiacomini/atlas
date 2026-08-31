#!/usr/bin/env python3
from datetime import date
from pathlib import Path
import json
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "atlas.sqlite"
OUT = ROOT / "data" / "media.manifest.json"

GROUPS = {
    "vehicle": ("vehicles.webp", "Ilustração editorial sobre a evolução dos automóveis"),
    "vehicle_instance": ("vehicles.webp", "Ilustração editorial sobre veículos históricos"),
    "person": ("people-industry.webp", "Ilustração editorial sobre pessoas da indústria automotiva"),
    "organization": ("people-industry.webp", "Ilustração editorial sobre organizações automotivas"),
    "brand": ("people-industry.webp", "Ilustração editorial sobre marcas e indústria automotiva"),
    "team": ("motorsport.webp", "Ilustração editorial sobre equipes e competição automobilística"),
    "technology": ("technology.webp", "Ilustração editorial de tecnologias automotivas"),
    "component": ("technology.webp", "Ilustração editorial de componentes automotivos"),
    "event": ("motorsport.webp", "Ilustração editorial sobre eventos da história automotiva"),
    "entry": ("motorsport.webp", "Ilustração editorial sobre inscrições em competições"),
    "competition": ("motorsport.webp", "Ilustração editorial sobre competição automobilística"),
    "season": ("motorsport.webp", "Ilustração editorial sobre temporadas de competição"),
    "regulation": ("motorsport.webp", "Ilustração editorial sobre regras e competição"),
    "facility": ("geography.webp", "Ilustração editorial sobre fábricas e lugares automotivos"),
    "place": ("geography.webp", "Ilustração editorial sobre a geografia automotiva"),
    "circuit": ("geography.webp", "Ilustração editorial sobre circuitos históricos"),
    "circuit_layout": ("geography.webp", "Ilustração editorial sobre traçados de circuitos"),
}

# O manifesto cobre as entidades editoriais, não o catálogo: uma identidade
# catalogada não tem verbete a ilustrar, e o contrato em tests/test_contracts.py
# exige que a contagem do manifesto seja exatamente a das não catalogadas.
QUERY = """
    SELECT id, canonical_name, entity_type FROM entity
    WHERE COALESCE(json_extract(metadata_json, '$.editorial_level'), 'editorial') != 'catalog'
    ORDER BY canonical_name
"""

# A data de verificação é preservada por entidade. Regenerar o manifesto não
# reverifica mídia nenhuma, e carimbar a data de hoje em 398 linhas afirmaria uma
# conferência que não aconteceu.
previous = {}
if OUT.is_file():
    previous = {item["entity_id"]: item.get("verified_on") for item in json.loads(OUT.read_text(encoding="utf-8"))["items"]}
TODAY = date.today().isoformat()

db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row
rows = []
for entity in db.execute(QUERY):
    filename, alt = GROUPS[entity["entity_type"]]
    rows.append({
        "entity_id": entity["id"],
        "entity_name": entity["canonical_name"],
        "file": f"media/editorial/{filename}",
        "thumbnail": f"media/editorial/{filename}",
        "media_type": "image/webp",
        "creator": "OpenAI image generation, directed and curated for Atlas",
        "source_url": "https://github.com/flpgiacomini/atlas",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "credit": "Ilustração original do projeto Atlas; gerada com OpenAI e revisada editorialmente.",
        "alt": f"{alt}; representação interpretativa associada a {entity['canonical_name']}.",
        "verified_on": previous.get(entity["id"]) or TODAY,
        "nature": "original_illustration",
        "historical_evidence": False,
    })
db.close()
OUT.write_text(json.dumps({"version": 1, "items": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"media_items": len(rows)}, ensure_ascii=False))
