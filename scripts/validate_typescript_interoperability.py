#!/usr/bin/env python3
"""Compare independently produced Python and TypeScript conformance outcomes.

The TypeScript reports MUST already exist. This script deliberately compares only
observable outcomes and historical assurance results; it does not share evaluator
code with the TypeScript track.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from reference_evaluator import evaluate_authority, resolve_identifier  # noqa: E402

TS_REPORT = ROOT / "artifacts" / "typescript" / "conformance-report.json"
TS_HISTORICAL = ROOT / "artifacts" / "typescript" / "historical-resolution-report.json"
PY_HISTORICAL = ROOT / "artifacts" / "historical-resolution" / "evidence-bundle.json"
OUT = ROOT / "artifacts" / "typescript" / "cross-runtime-report.json"


def python_outcome(vector: dict) -> str:
    if vector["check"] == "identifier_resolution":
        return resolve_identifier(vector["input"])[0]
    if vector["check"] == "authority_evaluation":
        return evaluate_authority(vector["input"])[0]
    raise ValueError(f"unsupported check: {vector['check']}")


def main() -> int:
    missing = [path for path in (TS_REPORT, TS_HISTORICAL, PY_HISTORICAL) if not path.exists()]
    if missing:
        raise SystemExit("Required assurance report missing: " + ", ".join(str(path.relative_to(ROOT)) for path in missing))

    ts = json.loads(TS_REPORT.read_text())
    ts_results = {item["vector_id"]: item for item in ts["results"]}
    deterministic = []

    for path in sorted((ROOT / "conformance" / "test-vectors").glob("TV-*.json")):
        vector = json.loads(path.read_text())
        py = python_outcome(vector)
        ts_item = ts_results.get(vector["vector_id"])
        ts_outcome = ts_item["actual"] if ts_item else None
        expected = vector["expected_outcome"]
        deterministic.append({
            "vector_id": vector["vector_id"],
            "expected": expected,
            "python": py,
            "typescript": ts_outcome,
            "equivalent": py == ts_outcome == expected,
        })

    py_hist = {item["id"]: item for item in json.loads(PY_HISTORICAL.read_text())["results"]}
    ts_hist = {item["id"]: item for item in json.loads(TS_HISTORICAL.read_text())["results"]}
    historical = []
    for vector_id in sorted(set(py_hist) | set(ts_hist)):
        py_item = py_hist.get(vector_id)
        ts_item = ts_hist.get(vector_id)
        equivalent = bool(
            py_item and ts_item
            and py_item["passed"] and ts_item["passed"]
            and py_item["reconstruction_status"] == ts_item["reconstruction_status"]
            and py_item["historical_effect"] == ts_item["historical_effect"]
        )
        historical.append({
            "vector_id": vector_id,
            "python_reconstruction_status": py_item.get("reconstruction_status") if py_item else None,
            "typescript_reconstruction_status": ts_item.get("reconstruction_status") if ts_item else None,
            "python_historical_effect": py_item.get("historical_effect") if py_item else None,
            "typescript_historical_effect": ts_item.get("historical_effect") if ts_item else None,
            "equivalent": equivalent,
        })

    deterministic_passed = sum(1 for item in deterministic if item["equivalent"])
    historical_passed = sum(1 for item in historical if item["equivalent"])
    total = len(deterministic) + len(historical)
    equivalent = deterministic_passed + historical_passed
    report = {
        "report_type": "arpa-cross-runtime-conformance",
        "arpa_baseline": "0.9.4",
        "implementations": ["ARPA Python reference/evidence path", "ARPA TypeScript v0.3.0"],
        "independence_boundary": "Implementations share normative artifacts and vectors but not behavioral implementation code.",
        "surfaces": {
            "deterministic_conformance": {"total": len(deterministic), "equivalent": deterministic_passed, "comparisons": deterministic},
            "historical_resolution": {"total": len(historical), "equivalent": historical_passed, "comparisons": historical},
        },
        "total": total,
        "equivalent": equivalent,
        "passed": equivalent == total,
        "limitations": [
            "Repository-owned TypeScript code is not evidence of external organisational independence.",
            "Historical comparison proves equivalent interpretation of the bounded v0.9.4 vector corpus; it is not yet network retrieval interoperability.",
            "Network-level interoperability is reported separately in artifacts/typescript/network-interoperability-report.json.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Cross-runtime equivalence: {equivalent}/{total} checks ({deterministic_passed}/{len(deterministic)} deterministic; {historical_passed}/{len(historical)} historical)")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
