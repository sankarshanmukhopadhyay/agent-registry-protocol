# ARPA → IETF Protocol Extraction Map

This file records which ARPA project surfaces feed the Internet-Draft and which
remain outside its normative boundary.

| ARPA surface | IETF treatment | Evidence / source |
|---|---|---|
| Identifier and namespace model | Core normative | `spec/agent-registry-protocol-v0.9.0.md`, `schemas/*` |
| Record envelope and agent model | Core normative | schemas and valid examples |
| Relationships | Core normative | `schemas/relationship.schema.json`, relationship registry |
| Delegation and authority | Core normative | v0.9.0 §18 + `spec/agent-registry-protocol-v0.9.1-hardening.md` §§1–5; authority schema and vectors |
| Temporal validity and event ordering | Core normative | v0.9.1 hardening §2; `ADV-003`–`ADV-005` |
| Authority outcome / `not_applicable` boundary | Core normative | v0.9.1 hardening §3; `ADV-016` |
| Recognition conflict | Core normative invariant | v0.9.1 hardening §4; `ADV-007`, `ADV-017` |
| Revocation effectiveness vs convergence | Core normative | v0.9.1 hardening §5; `ADV-006` |
| Decision reproducibility/checkpoints | Core normative | v0.9.1 hardening §6; `ADV-020` |
| Proof-input semantics | Core normative minimum | v0.9.1 hardening §7; proof-suite details remain extensible |
| Lifecycle/status | Core normative | lifecycle/status registries and vectors |
| Historical resolution | Core normative | historical schema, vectors, evidence |
| Query/HTTP behavior | Core normative | OpenAPI + reference implementations |
| Events | Core semantics; transport-neutral | AsyncAPI + event registry |
| Error handling | Core normative | error-code registry; RFC 9457 mapping |
| Federation/recognition | Minimal invariants only | detailed profile remains project-level |
| Multi-dimensional status composition | Project-level normative hardening | v0.9.1 hardening §8; IETF keeps non-affirmative invariant without project profile taxonomy |
| Pairwise continuity | Privacy/security invariant | v0.9.1 hardening §9; proof construction remains outside first I-D |
| Schema correction authority | Project change control | v0.9.1 hardening §10; not wire protocol text |
| Execution/decision receipts | Supporting evidence | potential future I-D |
| Governance, appeals, redress | Project-level / deployment profile | not first-draft protocol core |
| Conformance profiles | Supporting assurance | not normative in first I-D |
| A2A interoperability | Separate profile | not first-draft protocol core |
| TRQP projection | Separate profile | not first-draft protocol core |
| RAHP/governance assurance | Supporting evidence | not IETF protocol text |

## IETF source provenance for v0.9.1 hardening

The generated individual draft is assembled from two checked-in IETF authoring inputs:

1. `ietf/draft-sankarshan-agent-registry-protocol.md` — base protocol extraction; and
2. `ietf/fragments/adversarial-hardening.md` — protocol-core semantics imported from the v0.9.1 Candidate hardening amendment.

`scripts/build_ietf_draft.sh` inserts the hardening fragment immediately before the unnumbered `Acknowledgements` and back matter and then runs `kramdown-rfc` and `xml2rfc`. The fragment is therefore numbered protocol body text in generated RFCXML, TXT and HTML. Generated files remain derivative publication artifacts and are not committed as independent normative state.

## Non-implication and adversarial invariants retained in the I-D

1. Identity is not authority.
2. Key control is not accountability.
3. Capability is not permission.
4. Proof validity is not authority validity.
5. Federation is not governance recognition.
6. Stale, conflicting, unavailable, unsupported, incomparable, or unverifiable material authority is not affirmative authority.
7. Historical state is evidence, not by itself a legal determination.
8. Downstream authority is the semantic intersection of upstream authority and child-declared scope.
9. Omitted upstream constraints and prohibitions do not disappear downstream.
10. `not_applicable` cannot represent failure to establish required authority.
11. Effective revocation is non-affirmative even before enforcement convergence completes.
12. Unresolved conflict between simultaneously competent authoritative sources is non-affirmative.

## Change control

Every normative I-D change should identify:

- the originating ARPA requirement or issue;
- the affected I-D section;
- the executable test or inspection procedure, where objectively testable; and
- the evidence artifact expected from validation.

For the v0.9.1 hardening import, machine-readable requirement-to-vector traceability is recorded in `registries/adversarial-hardening-requirements-v0.9.1.json` and `conformance/test-vectors/adversarial/adversarial-authority-v0.9.1.json`.

This keeps IETF prose reviewable without making the I-D depend on repository-only tooling for normative interpretation.
