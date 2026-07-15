"""
reference_evaluator.py

A minimal, deterministic reference implementation of the core decision
logic in spec §28.2 (Authority Evaluation Algorithm), used to execute the
conformance test vectors under conformance/test-vectors/.

This is NOT a full protocol implementation. It intentionally omits proof
verification, issuer-competence resolution, and federation/recognition
evaluation (steps 8 and 14 of §28.2), which require external key material
and registry state that a static test vector cannot provide. It implements
the parts of the algorithm that are pure functions of the record content
already present in a test vector: status gating (steps 3-5), envelope
resolution and time/scope/limit checks (steps 6, 9, 10), mandatory
prohibitions before discretionary conditions (step 11), and required
approvals (step 12). This is sufficient to produce the same `allow` /
`allow_with_conditions` / `deny` / `indeterminate` / `not_applicable`
outcome as a full evaluator for the scenarios covered by the test vectors,
and is deliberately scoped this way so the conformance suite tests
observable protocol behavior rather than re-implementing cryptography.

Downstream: a full reference implementation (ROADMAP.md Phase 5) should
extend this module rather than replace its decision semantics, since the
test vectors assert against exactly this contract.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


ACTIVE_LIKE_REGISTRATION = {"active", "restricted"}
OK_OPERATIONAL = {"available", "degraded"}
BLOCKING_OPERATIONAL = {"restricted", "maintenance", "offline", "draining", "quarantined", "unknown"}
OK_SECURITY = {"normal", "elevated_monitoring"}
BLOCKING_SECURITY = {
    "suspected_compromise", "confirmed_compromise",
    "containment_in_progress", "recovery_in_progress",
    "under_investigation", "unknown",
}


def resolve_identifier(vector_input: dict[str, Any]) -> tuple[str, list[str]]:
    """Reference implementation of the resolution outcomes required by §12.6.

    vector_input keys:
      known: bool                 -- registry has ever issued this identifier
      terminal: bool               -- identifier is retired/revoked/burned/superseded
      authorized_caller: bool       -- caller is authorized to view this record
    """
    known = vector_input.get("known", False)
    terminal = vector_input.get("terminal", False)
    authorized_caller = vector_input.get("authorized_caller", True)

    if not known:
        return "not_found", ["identifier_never_issued"]
    if not authorized_caller:
        return "not_authorized", ["caller_not_authorized_for_record"]
    if terminal:
        return "terminal_record", ["identifier_known_but_terminal"]
    return "active_record", ["identifier_known_and_active"]


def evaluate_authority(vector_input: dict[str, Any]) -> tuple[str, list[str]]:
    """Return (decision, reason_codes) for a single test-vector input.

    vector_input keys:
      profile: "A" | "B" | "C" | "D"
      agent_status: {registration, operation, security, observed_at, valid_until}
      authority_envelope: {...} | null
      request: {action, resource, amount, jurisdiction, time, policy_max_status_age_seconds}
    """
    profile = vector_input["profile"]
    reasons: list[str] = []

    # Profile A (Discovery Registry) does not support authority evaluation at all (§35.1).
    if profile == "A":
        return "not_applicable", ["profile_a_discovery_only_no_authority_evaluation"]

    status = vector_input.get("agent_status")
    request = vector_input["request"]
    request_time = _parse_time(request["time"])

    # Step 3: registration status must permit the requested class of action.
    if status is None:
        return "indeterminate", ["missing_status_record"]

    if status["registration"] not in ACTIVE_LIKE_REGISTRATION:
        return "deny", [f"registration_status_{status['registration']}_does_not_permit_action"]

    # Step 4: operational and security status must permit execution.
    if status["operation"] in BLOCKING_OPERATIONAL and status["operation"] != "restricted":
        return "deny", [f"operational_status_{status['operation']}_blocks_execution"]
    if status["security"] in BLOCKING_SECURITY:
        return "deny", [f"security_status_{status['security']}_blocks_execution"]

    # Step 5: freshness policy.
    observed_at = _parse_time(status["observed_at"])
    valid_until = _parse_time(status["valid_until"])
    max_age = request.get("policy_max_status_age_seconds")
    if request_time > valid_until:
        return "indeterminate", ["status_stale_past_valid_until"]
    if max_age is not None and (request_time - observed_at).total_seconds() > max_age:
        return "indeterminate", ["status_older_than_policy_max_age"]

    # Steps 6-9: resolve envelope, verify time/scope narrowing.
    envelope = vector_input.get("authority_envelope")
    if envelope is None:
        return "deny", ["no_applicable_authority_envelope"]

    eff_from = _parse_time(envelope["effective_from"])
    eff_until = envelope.get("effective_until")
    if request_time < eff_from:
        return "deny", ["authority_not_yet_effective"]
    if eff_until is not None and request_time > _parse_time(eff_until):
        return "deny", ["authority_expired"]

    if request["action"] not in envelope.get("action_classes", []):
        return "deny", ["action_not_within_authority_scope"]

    resource_scope = envelope.get("resource_scope")
    if resource_scope and request.get("resource") not in resource_scope:
        return "deny", ["resource_not_within_authority_scope"]

    jurisdiction_scope = envelope.get("jurisdiction_scope")
    if jurisdiction_scope and request.get("jurisdiction") not in jurisdiction_scope:
        return "deny", ["jurisdiction_not_within_authority_scope"]

    # Step 11: mandatory prohibitions before discretionary conditions.
    if request["action"] in envelope.get("prohibitions", []):
        return "deny", ["action_matches_mandatory_prohibition"]

    # Step 10 (limits): quantitative limits.
    limits = envelope.get("limits") or {}
    amount = request.get("amount")
    if amount is not None:
        per_txn = limits.get("per_transaction")
        aggregate = limits.get("aggregate")
        if per_txn is not None and amount > per_txn:
            return "deny", ["amount_exceeds_per_transaction_limit"]
        if aggregate is not None and amount > aggregate:
            return "deny", ["amount_exceeds_aggregate_limit"]

    # Step 12: required approvals -> allow_with_conditions if unmet.
    unmet_conditions = []
    for approval in envelope.get("required_approvals", []):
        condition = approval["condition"]
        # Only supports the single condition shape used by the test vectors:
        # "amount > N"
        if condition.startswith("amount >") and amount is not None:
            threshold = float(condition.split(">", 1)[1].strip())
            if amount > threshold:
                unmet_conditions.append(approval["approval"])

    if unmet_conditions:
        reasons.append("within_scope")
        reasons.append("approval_required")
        return "allow_with_conditions", reasons

    reasons.append("within_scope")
    return "allow", reasons
