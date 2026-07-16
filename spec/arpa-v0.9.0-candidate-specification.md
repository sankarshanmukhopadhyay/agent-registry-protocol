# Agent Registry Protocol v0.9.0 Candidate Specification

## Status

This document defines the Candidate Specification release surface for ARPA v0.9.0. The detailed architecture remains in `draft-agent-registry-protocol-architecture.md`; this companion fixes the candidate requirements, conformance targets, evidence expectations and extension boundaries.

## Normative language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** are to be interpreted as described by BCP 14 when, and only when, they appear in all capitals.

## Candidate requirements

| ID | Requirement | Conformance target |
|---|---|---|
| ARPA-CAND-001 | Implementations MUST distinguish identity, authority, assurance, proof validity and lifecycle status. | Registry, consumer |
| ARPA-CAND-002 | Delegation MUST NOT expand the issuer's effective scope. | Evaluator |
| ARPA-CAND-003 | Recognition MUST be scoped, current, withdrawable and non-transitive unless explicitly declared. | Registry, evaluator |
| ARPA-CAND-004 | Technical federation MUST NOT imply governance recognition. | Federation participant |
| ARPA-CAND-005 | Revocation MUST produce durable evidence and MUST NOT be considered converged until applicable enforcement acknowledgements exist. | Publisher, consumer, enforcement point |
| ARPA-CAND-006 | Unknown, conflicting, stale or unavailable authority MUST resolve to deny or indeterminate, never implicit allow. | Evaluator |
| ARPA-CAND-007 | Events MUST be sequenceable, replayable, deduplicated and processable idempotently. | Event publisher, consumer |
| ARPA-CAND-008 | Proof validity MUST NOT be interpreted as authority validity. | Verifier, evaluator |
| ARPA-CAND-009 | Policy decisions MUST retain policy version, evaluated inputs, outcome, reason codes and evidence references. | Policy adapter |
| ARPA-CAND-010 | Implementation capability and conformance claims MUST be machine-readable and evidence-bounded. | Implementation |
| ARPA-CAND-011 | ARPA–TRQP projection support MUST be declared independently from ARPA and TRQP conformance. | Projection adapter |
| ARPA-CAND-012 | Projection MUST preserve scope and MUST NOT produce an affirmative result for revoked, suspended, expired or unresolved authority. | Projection adapter |

## Conformance targets

- Registry publisher
- Registry consumer/resolver
- Authority evaluator
- Event publisher
- Event consumer/enforcement point
- Proof verifier
- Policy adapter
- Federation participant
- ARPA–TRQP projection adapter

## Extension model

Extensions MUST use a registered namespace, MUST declare their version and authority, and MUST NOT redefine a core field. Unknown extensions MUST be retained or ignored according to the applicable profile and MUST NOT cause an affirmative decision by default.

## Evidence model

Every objectively testable requirement maps to a positive or negative vector and an evidence output. Review-only requirements map to an inspectable checklist. The release manifest identifies each report and digest.
