#!/usr/bin/env python3
"""Validate the informative KYA-OS -> ARPA interoperability profile.

This validator deliberately does not verify KYA-OS cryptography. It treats
`proof_verified` as an external evidence input and proves that ARPA authority
outcomes remain independently constrained by ARPA governance state.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "conformance" / "kya-os"
SCHEMA = PROFILE / "vector-schema.json"
VECTORS = PROFILE / "vectors.json"


def expected_decision(vector: dict) -> tuple[str, str, str | None]:
    evidence = vector["external_evidence"]
    context = vector["arpa_context"]

    if not evidence["proof_verified"]:
        return "denied", "reject", "external-proof-unverified"
    if not evidence["delegation"]["projection_lossless"]:
        return "projection-rejected", "reject", "semantic-projection-loss"
    if context.get("historical_authorized") is False:
        return "denied", "deny", "not-authorized-at-evaluation-time"
    if context["agent_state"] == "suspended":
        return "denied", "deny", "agent-suspended"
    if context["agent_state"] == "revoked":
        finding = "revoked-enforcement-convergence-incomplete" if not context["enforcement_converged"] else "agent-revoked"
        return "denied", "deny", finding
    if not context["delegator_competent"]:
        return "denied", "deny", "delegator-not-competent"
    if not context["recognized_authority_source"]:
        return "denied", "deny", "no-recognized-authority-source"
    if context["authority_conflict"] and not context.get("conflict_resolved", False):
        return "indeterminate", "indeterminate", "unresolved-authority-conflict"
    if not context["scope_allows_action"]:
        return "denied", "deny", "action-outside-governed-scope"
    return "authorized", "allow", None


def validate_vector(vector: dict, validator: Draft202012Validator) -> list[str]:
    errors: list[str] = []
    vector_id = vector.get("vector_id", "<unknown>")

    for error in sorted(validator.iter_errors(vector), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.path)
        errors.append(f"{vector_id}: schema {path}: {error.message}")

    if errors:
        return errors

    expected = vector["expected"]
    proof_result = "verified" if vector["external_evidence"]["proof_verified"] else "rejected"
    if expected["proof_result"] != proof_result:
        errors.append(f"{vector_id}: proof_result must reflect external verification independently of ARPA authority")

    authority_result, outcome, finding = expected_decision(vector)
    if expected["authority_result"] != authority_result:
        errors.append(f"{vector_id}: expected authority_result={expected['authority_result']} but ARPA boundary requires {authority_result}")
    if expected["outcome"] != outcome:
        errors.append(f"{vector_id}: expected outcome={expected['outcome']} but ARPA boundary requires {outcome}")
    if finding and expected.get("finding") != finding:
        errors.append(f"{vector_id}: expected finding must be {finding}")

    # Proof validity must never be treated as a sufficient authorization rule.
    if vector["external_evidence"]["proof_verified"] and expected["authority_result"] == "authorized":
        context = vector["arpa_context"]
        independent_requirements = [
            context["agent_state"] == "active",
            context["delegator_competent"],
            context["recognized_authority_source"],
            context["scope_allows_action"],
            not context["authority_conflict"] or context.get("conflict_resolved", False),
            context.get("historical_authorized", True),
        ]
        if not all(independent_requirements):
            errors.append(f"{vector_id}: verified proof cannot synthesize missing ARPA authority")

    if not vector["falsifier"].strip():
        errors.append(f"{vector_id}: falsifier must be explicit")
    return errors


def main() -> int:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    vectors = json.loads(VECTORS.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    errors: list[str] = []
    ids: set[str] = set()
    propositions: set[str] = set()
    for vector in vectors:
        vector_id = vector.get("vector_id")
        if vector_id in ids:
            errors.append(f"duplicate vector id: {vector_id}")
        ids.add(vector_id)
        propositions.add(vector.get("proposition", ""))
        errors.extend(validate_vector(vector, validator))

    required_ids = {f"KYA-ARPA-{n:02d}" for n in range(1, 11)}
    missing = required_ids - ids
    if missing:
        errors.append(f"missing required issue #12 vectors: {sorted(missing)}")

    required_propositions = {"PQ-1", "PQ-2", "PQ-3", "PQ-4"}
    if not required_propositions.issubset(propositions):
        errors.append(f"missing proposition coverage: {sorted(required_propositions - propositions)}")

    verified_but_denied = any(
        v["external_evidence"]["proof_verified"] and v["expected"]["outcome"] in {"deny", "indeterminate", "reject"}
        for v in vectors
    )
    if not verified_but_denied:
        errors.append("corpus must prove that verified external evidence can still fail ARPA authority evaluation")

    if errors:
        print("KYA-OS -> ARPA profile validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"KYA-OS -> ARPA profile validation passed: {len(vectors)} vectors; PQ-1..PQ-4 covered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
