# Conformance Profile D: High-Assurance or Fiduciary Registry

Source: spec §35.4, Appendix D.1–D.4. Includes Profile C. Suitable for public services, healthcare, finance, legal services, identity-affecting systems, or fiduciary contexts.

## Required record families (schemas/), additive to Profile C

| Record family | Schema |
|---|---|
| Recognition Record (multi-party/independent governance) | `schemas/recognition.schema.json` |

No new record family is introduced solely for Profile D beyond Recognition; Profile D instead tightens *which* fields of already-defined records are mandatory (e.g. `prohibitions`, `redress_process`) and adds deployment-level controls (runtime attestation, key separation, threshold administration) that are operational rather than record-shaped — see the unchecked items below.

## Test matrix

| Vector ID | Case type | Scenario | Expected outcome | Spec refs |
|---|---|---|---|---|
| `TV-D-01` | Positive (grant) | Fiduciary `portfolio.analyze`, in scope/jurisdiction, not prohibited | `allow` | §4.6, §18.2 |
| `TV-D-02` | Negative (block) | Capability includes `asset.transfer`; envelope declares it a mandatory prohibition | `deny` | §6.3 (capability ≠ permission), §28.2 step 11 |
| `TV-D-03` | Negative (block) | Request evaluated after `effective_until` | `deny` | §28.2 step 6, §28.10 |

## Checklist (Appendix D.1–D.4)

All of Profile C, plus:

- [x] Accountable institution — `relationship.schema.json#relationship_type` = `accountable_to`, required at Profile B and re-asserted for Profile D
- [ ] Beneficiary and duty metadata — `relationship.schema.json#relationship_type` includes `benefits`; no dedicated duty-metadata schema yet (Open Issue §40.15, liability/duty metadata)
- [x] Explicit prohibitions — `authority-envelope.schema.json#prohibitions`, `TV-D-02`
- [ ] Independent assurance — governance-process requirement (assessor independence), not schema-testable
- [ ] Runtime attestation — `deployment.schema.json#runtime_identifiers` records the identifier; the attestation *process* (§20.10) is deployment-specific
- [ ] Key separation — `key-binding.schema.json#intended_use` enum enforces declared separation per key binding; cross-key uniqueness (no two administrative keys sharing a use) is a registry-level invariant, not a single-record schema constraint
- [ ] Threshold administration — governance/operational, not schema-testable
- [ ] Continuous monitoring — governance/operational, not schema-testable
- [ ] Emergency suspension — `event.schema.json#event_type` includes `agent.suspended`; the emergency-vs-ordinary distinction is a `reason_code` convention, not yet a controlled vocabulary (Open Issue candidate)
- [ ] Multi-party governance — `schemas/recognition.schema.json` supports multi-domain recognition; multi-party *admission* governance is process-level
- [ ] Transparency reporting — spec §32.2, process-level
- [ ] Independent appeal — `governance.schema.json#appeal_procedure`, `#dispute_venue`
- [ ] Evidence retention — spec §25.6, governance-policy-level
- [ ] Essential-service continuity — spec §27.6, deployment-specific
- [ ] External audit — spec §32.3, process-level

Profile D has the largest share of unchecked (process-level, not schema-testable) items of any profile. This is expected: Profile D's incremental requirements over Profile C are disproportionately about *institutional* controls (independent assessors, threshold administration, external audit) rather than *record-shape* controls, and a static conformance suite can only assert the latter. This gap is noted explicitly rather than papered over with a schema that can't actually test the requirement.
