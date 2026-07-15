# Conformance Profile C: Delegated Authority Registry

Source: spec §35.3, Appendix D.1–D.3. Includes Profile B. Suitable for agents that transact, commit resources, exercise delegated permissions, or act for principals.

## Required record families (schemas/), additive to Profile B

| Record family | Schema |
|---|---|
| Authority Envelope | `schemas/authority-envelope.schema.json` |
| Decision Receipt | `schemas/decision-receipt.schema.json` |

## Test matrix

| Vector ID | Case type | Scenario | Expected outcome | Spec refs |
|---|---|---|---|---|
| `TV-C-01` | Positive (grant) | Procurement `purchase.submit`, amount below approval threshold and within per-transaction limit | `allow` | §18.2, §28.2 |
| `TV-C-02` | Positive (grant, conditional) | Amount above the approval threshold, still within limits | `allow_with_conditions` enumerating the unmet approval | §18.5 |
| `TV-C-03` | Negative (block) | Amount exceeds the envelope's `per_transaction` limit | `deny` | §18.4 (delegation narrowing), §28.2 step 10 |

## Checklist (Appendix D.1–D.3)

All of Profile B, plus:

- [x] Authority envelopes — `schemas/authority-envelope.schema.json`
- [x] Delegation chains — dedicated positive and negative multi-hop narrowing vectors are published as `EV-11` and `EV-12`.
- [x] Delegation narrowing validation — `TV-C-03` (limit narrowing)
- [x] Authority evaluation — `scripts/reference_evaluator.py::evaluate_authority`, all `TV-C-*`
- [x] Decision receipts — `schemas/decision-receipt.schema.json`, including the `allow_with_conditions` ⇒ non-empty `conditions` constraint (`examples/invalid/decision-receipt.json`)
- [ ] Runtime enforcement integration — deployment-specific, not schema-testable
- [ ] Cascade revocation — `authority-envelope.schema.json#revocation.cascade` is schema-validated for presence and enum membership; end-to-end cascade behavior requires a stateful registry and is out of scope for static test vectors
- [x] Approval conditions — `TV-C-02`
- [x] Quantitative limits — `TV-C-01`, `TV-C-03`
- [ ] Revocation propagation target — governance/SLA-level (§39.5), not schema-testable
- [ ] Enforcement acknowledgement — deployment-specific, not schema-testable
