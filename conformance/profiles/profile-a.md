# Conformance Profile A: Discovery Registry

Source: spec §35.1, Appendix D.1. Suitable for low-risk informational agents.

## Required record families (schemas/)

| Record family | Schema |
|---|---|
| Agent Core Record | `schemas/agent-core.schema.json` |
| Relationship Record (controller/operator) | `schemas/relationship.schema.json` |
| Service Endpoint Record | `schemas/service-endpoint.schema.json` |
| Key Binding Record | `schemas/key-binding.schema.json` |
| Governance Record (reference only) | `schemas/governance.schema.json` |

Profile A does **not** require Authority Envelope, Assurance Claim, Decision Receipt, or Execution Receipt records. A Profile A registry that returns an authority evaluation decision has exceeded its declared profile (§35.5) and must instead return `not_applicable`.

## Test matrix

Executable via `python3 scripts/validate_test_vectors.py`. Every row below has a corresponding file in `conformance/test-vectors/`.

| Vector ID | Case type | Scenario | Expected outcome | Spec refs |
|---|---|---|---|---|
| `TV-A-01` | Positive (grant) | Known, non-terminal identifier, authorized caller | `active_record` | §12.6 |
| `TV-A-02` | Negative (block) | Identifier never issued by the registry | `not_found` | §12.6 |
| `TV-A-03` | Negative (block) | Known but retired/revoked/superseded identifier | `terminal_record` (MUST NOT be `not_found`) | §12.6 |

## Checklist (Appendix D.1)

- [x] Persistent non-reassignable agent identifiers — `schemas/agent-core.schema.json#agent_id`, ABNF at spec §12.2
- [x] Historical resolution — `TV-A-03`
- [x] Core record — `schemas/agent-core.schema.json`
- [x] Explicit operator or controller relationship — `schemas/relationship.schema.json`
- [x] Lifecycle state machine — `agent-core.schema.json#registration_status` enum, spec §20.1
- [x] Governance metadata — `schemas/governance.schema.json`
- [ ] Secure query transport — deployment-specific; not schema-testable (see `conformance/README.md`)
- [x] Structured errors — spec §34.2, §34.3 (HTTP mapping)
- [x] Provenance and freshness — `schemas/status.schema.json` required fields
- [ ] Tamper-evident audit — deployment-specific
- [x] Extension handling — spec §13.8, §33.5
- [ ] Incident process — governance-level, not schema-testable
- [x] Conformance declaration — spec §35.5; see `conformance/README.md`
