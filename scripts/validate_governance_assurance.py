from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VECTORS = ROOT / "conformance" / "test-vectors" / "governance-assurance"
OUT = ROOT / "artifacts" / "governance-assurance"
HIGH_IMPACT = {
    "change_accountable_entity", "ownership_like_transfer", "security_restoration_after_compromise",
    "replace_recovery_keys", "modify_governance_framework", "broad_authority_issuance",
    "remove_critical_prohibition", "delete_or_redact_evidence"
}

def evaluate(v):
    c, i = v["control"], v["input"]
    if c == "administrative_authorization":
        if i.get("profile") in {"C", "D"} and i.get("operation") in HIGH_IMPACT:
            if len(set(i.get("approvals", []))) < int(i.get("required_approvals", 2)):
                return {"outcome": "deny", "reason": "ARPA-ADMIN-THRESHOLD-NOT-MET"}
        return {"outcome": "allow"}
    if c == "revocation_convergence":
        required, ack = set(i.get("required_enforcement_points", [])), set(i.get("acknowledged", []))
        if required.issubset(ack): return {"outcome": "converged"}
        return {"outcome": "not_converged", "reason": "ARPA-REVOCATION-NOT-CONVERGED"}
    if c == "federation_recognition":
        if not i.get("recognition_explicit") or not i.get("recognition_current"):
            return {"outcome": "deny", "reason": "ARPA-FEDERATION-NOT-RECOGNIZED"}
        statuses = set(i.get("source_statuses", []))
        if len(statuses) > 1 and not i.get("precedence_rule"):
            return {"outcome": "indeterminate", "reason": "ARPA-CONFLICTING-STATUS"}
        return {"outcome": "allow"}
    if c == "discovery_disclosure":
        caller = i.get("caller_class")
        visible = []
        for r in i.get("records", []):
            cls = r.get("disclosure_class", "public")
            if cls == "public" or (caller != "unauthenticated" and cls != "private"):
                visible.append(r["id"])
        return {"visible_ids": visible}
    if c == "compromise_restoration":
        approvals = set(i.get("approvals", []))
        if i.get("prior_status") != "confirmed_compromise": return {"outcome": "not_applicable"}
        if not i.get("fresh_security_evidence") or len(approvals) < int(i.get("required_approvals", 2)):
            return {"outcome": "deny_restoration", "reason": "ARPA-RECOVERY-ASSURANCE-INCOMPLETE"}
        return {"outcome": "allow_restoration"}
    raise ValueError(f"unknown control {c}")

def main():
    manifest = json.loads((VECTORS / "manifest.json").read_text())
    results, passed = [], 0
    for name in manifest["vectors"]:
        v = json.loads((VECTORS / name).read_text())
        actual, expected = evaluate(v), v["expected"]
        ok = actual == expected
        passed += int(ok)
        results.append({"id": v["id"], "file": name, "passed": ok, "expected": expected, "actual": actual})
        print(f"[{'OK' if ok else 'FAIL'}] {v['id']} {name}: {actual}")
    OUT.mkdir(parents=True, exist_ok=True)
    report = {
        "suite": manifest["suite"], "implementation_release": "0.9.5+unreleased",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "passed": passed, "total": len(results), "results": results,
        "assurance_boundary": "Repository-owned control logic and fixtures; not independent certification or production operational evidence."
    }
    (OUT / "evidence-bundle.json").write_text(json.dumps(report, indent=2) + "\n")
    if passed != len(results): raise SystemExit(1)
    print(f"validate_governance_assurance.py: {passed}/{len(results)} governance-assurance vectors passed")

if __name__ == "__main__": main()
