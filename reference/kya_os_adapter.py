"""Informative KYA-OS -> ARPA evidence adapter boundary.

This module does not verify KYA-OS cryptography. Callers must supply the result of
external verification separately. ARPA then evaluates governance state without
allowing proof validity to synthesize authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GovernedDecision:
    proof_result: str
    authority_result: str
    outcome: str
    finding: str | None = None

    def as_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "proof_result": self.proof_result,
            "authority_result": self.authority_result,
            "outcome": self.outcome,
        }
        if self.finding:
            data["finding"] = self.finding
        return data


def evaluate_external_evidence(external_evidence: dict[str, Any], arpa_context: dict[str, Any]) -> GovernedDecision:
    """Evaluate externally verified evidence against ARPA governance state.

    The order is intentional: unverifiable or lossy evidence is rejected before
    authority inference, then historical/lifecycle/competence/recognition/scope
    conditions are evaluated. Unresolved authority conflict remains indeterminate.
    """
    if not external_evidence["proof_verified"]:
        return GovernedDecision("rejected", "denied", "reject", "external-proof-unverified")

    if not external_evidence["delegation"]["projection_lossless"]:
        return GovernedDecision("verified", "projection-rejected", "reject", "semantic-projection-loss")

    if arpa_context.get("historical_authorized") is False:
        return GovernedDecision("verified", "denied", "deny", "not-authorized-at-evaluation-time")

    if arpa_context["agent_state"] == "suspended":
        return GovernedDecision("verified", "denied", "deny", "agent-suspended")

    if arpa_context["agent_state"] == "revoked":
        finding = "agent-revoked"
        if not arpa_context["enforcement_converged"]:
            finding = "revoked-enforcement-convergence-incomplete"
        return GovernedDecision("verified", "denied", "deny", finding)

    if not arpa_context["delegator_competent"]:
        return GovernedDecision("verified", "denied", "deny", "delegator-not-competent")

    if not arpa_context["recognized_authority_source"]:
        return GovernedDecision("verified", "denied", "deny", "no-recognized-authority-source")

    if arpa_context["authority_conflict"] and not arpa_context.get("conflict_resolved", False):
        return GovernedDecision("verified", "indeterminate", "indeterminate", "unresolved-authority-conflict")

    if not arpa_context["scope_allows_action"]:
        return GovernedDecision("verified", "denied", "deny", "action-outside-governed-scope")

    finding = "narrowed-subdelegation" if external_evidence["delegation"].get("depth", 0) > 0 else None
    return GovernedDecision("verified", "authorized", "allow", finding)
