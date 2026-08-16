#!/usr/bin/env python3
"""Compare independently produced Python and TypeScript conformance outcomes.

The TypeScript report MUST already exist. This script deliberately compares only
observable outcomes; it does not share evaluator code with the TypeScript track.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from reference_evaluator import evaluate_authority, resolve_identifier  # noqa: E402

TS_REPORT = ROOT / "artifacts" / "typescript" / "conformance-report.json"
OUT = ROOT / "artifacts" / "typescript" / "cross-runtime-report.json"


def python_outcome(vector: dict) -> str:
    if vector["check"] == "identifier_resolution":
        return resolve_identifier(vector["input"])[0]
    if vector["check"] == "authority_evaluation":
        return evaluate_authority(vector["input"])[0]
    raise ValueError(f"unsupported check: {vector['check']}")


def main() -> int:
    if not TS_REPORT.exists():
        raise SystemExit("TypeScript conformance report missing; run `make typescript-check` first")

    ts = json.loads(TS_REPORT.read_text())
    ts_results = {item["vector_id"]: item for item in ts["results"]}
    comparisons = []

    for path in sorted((ROOT / "conformance" / "test-vectors").glob("TV-*.json")):
        vector = json.loads(path.read_text())
        py = python_outcome(vector)
        ts_item = ts_results.get(vector["vector_id"])
        ts_outcome = ts_item["actual"] if ts_item else None
        expected = vector["expected_outcome"]
        comparisons.append({
            "vector_id": vector["vector_id"],
            "expected": expected,
            "python": py,
            "typescript": ts_outcome,
            "equivalent": py == ts_outcome == expected,
        })

    report = {
        "report_type": "arpa-cross-runtime-conformance",
        "arpa_baseline": "0.9.4",
        "implementations": ["ARPA Python reference evaluator", "ARPA TypeScript v0.1.0"],
        "independence_boundary": "Implementations share normative artifacts and vectors but not behavioral implementation code.",
        "total": len(comparisons),
        "equivalent": sum(1 for item in comparisons if item["equivalent"]),
        "passed": all(item["equivalent"] for item in comparisons),
        "comparisons": comparisons,
        "limitations": [
            "Repository-owned TypeScript code is not evidence of external organisational independence.",
            "Comparison covers the deterministic shared conformance-vector surface only.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Cross-runtime equivalence: {report['equivalent']}/{report['total']} vectors")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
