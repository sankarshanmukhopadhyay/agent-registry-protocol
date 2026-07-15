# Conformance Profile B: Accountable Agent Registry

Source: spec §35.2, Appendix D.1–D.2. Includes Profile A. Suitable for agents that access protected data, produce consequential recommendations, or modify workflows.

## Required record families (schemas/), additive to Profile A

| Record family | Schema |
|---|---|
| Agent Version Record | `schemas/agent-version.schema.json` |
| Deployment Record | `schemas/deployment.schema.json` |
| Assurance Claim | `schemas/assurance-claim.schema.json` |
| Execution Receipt (consequential actions) | `schemas/execution-receipt.schema.json` |
| Event Record | `schemas/event.schema.json` |

## Test matrix

| Vector ID | Case type | Scenario | Expected outcome | Spec refs |
|---|---|---|---|---|
| `TV-B-01` | Positive (grant) | Active/available/normal agent, action within envelope scope | `allow` | §28.2 |
| `TV-B-02` | Negative (block) | Registration status `suspended` | `deny` | §20.1, §28.2 step 3 |
| `TV-B-03` | Negative (block) | Status observed_at older than relying policy's `policy_max_status_age_seconds` | `indeterminate` | §20.11, §28.2 step 5, `ARPA-STATUS-STALE` |

## Checklist (Appendix D.1 + D.2)

All of Profile A, plus:

- [x] Version records — `schemas/agent-version.schema.json`
- [x] Deployment identifiers — `schemas/deployment.schema.json`
- [x] Accountability relationships — `relationship.schema.json#relationship_type` = `accountable_to`
- [ ] Structured capability records — capability declaration (§19.2) is currently prose-only; no dedicated schema yet (tracked in `schemas/README.md` "Not yet scheduled")
- [x] Assurance claims — `schemas/assurance-claim.schema.json`
- [x] Incident states — `status.schema.json#security` enum (§20.9)
- [x] Point-in-time queries — `TV-B-03` (freshness), spec §28.5
- [x] Execution receipts — `schemas/execution-receipt.schema.json`
- [x] Event subscriptions — `schemas/event.schema.json`
- [ ] Redress metadata — see `schemas/governance.schema.json#redress_process`; a dedicated Redress Record schema is not yet published (spec §27.5 marks fields SHOULD, not MUST)
