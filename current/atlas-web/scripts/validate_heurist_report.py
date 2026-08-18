from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT.parents[1] / "handoff" / "heurist-result.json"
REQUIREMENTS = {
    "entity",
    "temporal_relation",
    "conflict_901_911",
    "source_evidence",
    "entry_917",
    "genealogy",
    "filters",
    "map",
    "network",
    "round_trip",
}


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_REPORT
    report = json.loads(path.read_text(encoding="utf-8"))
    checks = report.get("checks", {})
    errors: list[str] = []
    missing = sorted(REQUIREMENTS - set(checks))
    if missing:
        errors.append(f"requisitos ausentes: {', '.join(missing)}")
    invalid = sorted(key for key, value in checks.items() if key in REQUIREMENTS and not isinstance(value, bool))
    if invalid:
        errors.append(f"resultados não booleanos: {', '.join(invalid)}")
    score = sum(checks.get(key) is True for key in REQUIREMENTS)
    critical_loss = report.get("critical_semantic_loss")
    status = report.get("status")
    approved = status == "completed" and score >= 8 and critical_loss is False and not errors
    if status == "completed":
        for field in ("instance_url", "heurist_version", "executed_at", "executor", "duration_minutes"):
            if not report.get(field):
                errors.append(f"campo obrigatório ausente: {field}")
        pilots = report.get("pilots", [])
        if len(pilots) != 5:
            errors.append("o relatório concluído deve registrar exatamente cinco pilotos")
        approved = score >= 8 and critical_loss is False and not errors
    result = {"passed": approved, "status": status, "score": score, "critical_semantic_loss": critical_loss, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if approved else 1


if __name__ == "__main__":
    raise SystemExit(main())
