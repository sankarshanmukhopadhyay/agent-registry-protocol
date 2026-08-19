#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
VECTORS = ROOT / "conformance" / "test-vectors" / "operational-resilience"
OUT = ROOT / "artifacts" / "operational-resilience"
SCHEMAS = ROOT / "schemas"

def evaluate(v):
    c, i = v["control"], v["input"]
    if c == "retry_safety":
        if i.get("attempts", 0) > i.get("aggregate_budget", 0):
            return {"outcome":"deny","reason":"ARPA-RESILIENCE-RETRY-BUDGET-EXCEEDED"}
        if i.get("consequential") and (not i.get("stable_operation_identity") or not i.get("idempotency_identity_preserved")):
            return {"outcome":"deny","reason":"ARPA-RESILIENCE-OPERATION-IDENTITY-UNSTABLE"}
        return {"outcome":"allow","side_effects_max":1 if i.get("consequential") else i.get("attempts",1)}
    if c == "failover_safety":
        if i.get("admission_control") and i.get("fanout_bounded") and i.get("retry_budget_enforced"):
            return {"outcome":"bounded_degradation"}
        return {"outcome":"unsafe_amplification"}
    if c == "recovery_hysteresis":
        return {"outcome":"restore_healthy" if i.get("stabilization_criterion_met") else "remain_recovering"}
    if c == "event_isolation":
        if i.get("quarantine_supported") and i.get("ordering_scope") != "global":
            return {"outcome":"progress","quarantined":[i["poison_event"]],"processable":[i["unrelated_consequential_event"]]}
        return {"outcome":"blocked"}
    if c == "ack_order":
        if i.get("consequential") and i.get("ack_requested") and not i.get("durable_handoff_complete"):
            return {"outcome":"withhold_ack","reason":"ARPA-RESILIENCE-DURABLE-HANDOFF-INCOMPLETE"}
        return {"outcome":"ack"}
    if c == "dependency_amplification":
        if not i.get("freshness_bound_preserved"):
            return {"outcome":"deny","reason":"ARPA-RESILIENCE-FRESHNESS-BOUND-VIOLATED"}
        if i.get("upstream_requests", 0) <= i.get("declared_max_amplification", 0):
            return {"outcome":"allow"}
        return {"outcome":"deny","reason":"ARPA-RESILIENCE-DEPENDENCY-AMPLIFICATION"}
    if c == "load_progress":
        if i.get("safety_critical") and (not i.get("reserved_or_prioritized_capacity") or not i.get("progress_observed")):
            return {"outcome":"deny","reason":"ARPA-RESILIENCE-SAFETY-CRITICAL-STARVATION"}
        return {"outcome":"allow"}
    raise ValueError(f"unknown control {c}")

def schema_registry():
    resources=[]
    for p in SCHEMAS.rglob("*.schema.json"):
        doc=json.loads(p.read_text()); r=Resource.from_contents(doc)
        if r.id(): resources.append((r.id(),r))
    return Registry().with_resources(resources)

def main():
    manifest=json.loads((VECTORS/"manifest.json").read_text())
    results=[]; passed=0
    for name in manifest["vectors"]:
        v=json.loads((VECTORS/name).read_text()); actual=evaluate(v); expected=v["expected"]; ok=actual==expected
        passed += int(ok); results.append({"id":v["id"],"file":name,"passed":ok,"expected":expected,"actual":actual})
        print(f"[{'OK' if ok else 'FAIL'}] {v['id']} {name}: {actual}")
    schema=json.loads((SCHEMAS/"operational-resilience-declaration.schema.json").read_text())
    valid=json.loads((ROOT/"examples/valid/operational-resilience-declaration.json").read_text())
    errors=list(Draft202012Validator(schema, registry=schema_registry()).iter_errors(valid))
    if errors:
        for e in errors: print(f"schema: {e.json_path}: {e.message}")
        raise SystemExit(1)
    report={
      "suite":manifest["suite"],"implementation_release":"0.9.5+unreleased",
      "generated_at":datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),
      "passed":passed,"total":len(results),"results":results,
      "assurance_boundary":"Modeled repository assurance for declared resilience outcomes; not production load certification, infrastructure certification, or independent assurance."
    }
    OUT.mkdir(parents=True,exist_ok=True); (OUT/"evidence-bundle.json").write_text(json.dumps(report,indent=2)+"\n")
    if passed != len(results): raise SystemExit(1)
    print(f"validate_operational_resilience.py: {passed}/{len(results)} operational-resilience vectors passed")
if __name__=='__main__': main()
