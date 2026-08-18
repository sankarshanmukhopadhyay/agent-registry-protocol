# ARPA → IETF Protocol Extraction Map

This file records which ARPA project surfaces feed the Internet-Draft and which
remain outside its normative boundary.

| ARPA surface | IETF treatment | Evidence / source |
|---|---|---|
| Identifier and namespace model | Core normative | `spec/agent-registry-protocol-v0.9.0.md`, `schemas/*` |
| Record envelope and agent model | Core normative | schemas and valid examples |
| Relationships | Core normative | `schemas/relationship.schema.json`, relationship registry |
| Delegation and authority | Core normative | `schemas/authority-envelope.schema.json`, conformance vectors |
| Lifecycle/status | Core normative | lifecycle/status registries and vectors |
| Historical resolution | Core normative | historical schema, vectors, evidence |
| Query/HTTP behavior | Core normative | OpenAPI + reference implementations |
| Events | Core semantics; transport-neutral | AsyncAPI + event registry |
| Error handling | Core normative | error-code registry; RFC 9457 mapping |
| Federation/recognition | Minimal invariants only | detailed profile remains project-level |
| Execution/decision receipts | Supporting evidence | potential future I-D |
| Governance, appeals, redress | Project-level / deployment profile | not first-draft protocol core |
| Conformance profiles | Supporting assurance | not normative in first I-D |
| A2A interoperability | Separate profile | not first-draft protocol core |
| TRQP projection | Separate profile | not first-draft protocol core |
| RAHP/governance assurance | Supporting evidence | not IETF protocol text |

## Non-implication invariants retained in the I-D

1. Identity is not authority.
2. Key control is not accountability.
3. Capability is not permission.
4. Proof validity is not authority validity.
5. Federation is not governance recognition.
6. Stale, conflicting, unavailable, or unverifiable material authority is not affirmative authority.
7. Historical state is evidence, not by itself a legal determination.

## Change control

Every normative I-D change should identify:

- the originating ARPA requirement or issue;
- the affected I-D section;
- the executable test or inspection procedure, where objectively testable; and
- the evidence artifact expected from validation.

This keeps IETF prose reviewable without making the I-D depend on repository-only
tooling for normative interpretation.
