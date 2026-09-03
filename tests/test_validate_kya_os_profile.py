import json
from pathlib import Path

from scripts.validate_kya_os_profile import PROFILE, expected_decision


def _vectors():
    return json.loads((PROFILE / "vectors.json").read_text(encoding="utf-8"))


def test_verified_proof_does_not_imply_authority():
    vectors = {v["vector_id"]: v for v in _vectors()}
    authority_result, outcome, finding = expected_decision(vectors["KYA-ARPA-02"])
    assert vectors["KYA-ARPA-02"]["external_evidence"]["proof_verified"] is True
    assert (authority_result, outcome, finding) == ("denied", "deny", "delegator-not-competent")


def test_unresolved_authority_conflict_fails_indeterminate():
    vector = next(v for v in _vectors() if v["vector_id"] == "KYA-ARPA-05")
    assert expected_decision(vector) == ("indeterminate", "indeterminate", "unresolved-authority-conflict")


def test_semantic_projection_loss_is_rejected_before_authorization():
    vector = next(v for v in _vectors() if v["vector_id"] == "KYA-ARPA-08")
    assert expected_decision(vector) == ("projection-rejected", "reject", "semantic-projection-loss")


def test_revocation_and_enforcement_convergence_are_distinct():
    vector = next(v for v in _vectors() if v["vector_id"] == "KYA-ARPA-04")
    assert vector["arpa_context"]["enforcement_converged"] is False
    assert expected_decision(vector) == ("denied", "deny", "revoked-enforcement-convergence-incomplete")


def test_historical_evaluation_is_not_rewritten_by_current_proof():
    vector = next(v for v in _vectors() if v["vector_id"] == "KYA-ARPA-06")
    assert expected_decision(vector) == ("denied", "deny", "not-authorized-at-evaluation-time")
