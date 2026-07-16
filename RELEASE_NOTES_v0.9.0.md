# ARPA v0.9.0 — Candidate Specification and Governed Query Interoperability

ARPA v0.9.0 advances the protocol from a same-repository interoperability draft to a Candidate Specification with stable requirements, broader executable assurance and a documented relationship with TRQP.

## Highlights

- Candidate requirements with stable identifiers and conformance targets.
- Hardened delegation, recognition, lifecycle and revocation-convergence rules.
- Separately structured reference and independent projection adapters.
- Networked metadata discovery and durable event replay, deduplication and checkpoint evidence.
- ARPA–TRQP query-projection architecture, machine-readable mapping and 13 positive/negative vectors.
- Compatibility matrix, migration guide, requirement traceability and Candidate Specification evidence bundle.

## Compatibility

The existing ARPA record-schema track remains compatible. v0.9.0 adds Candidate Specification requirements and optional capability declarations. TRQP projection support is optional and independently versioned.

## Assurance boundary

This release is not v1.0. The bundled implementation paths are maintained in one repository; network testing uses loopback endpoints; durable-event testing uses SQLite; and the TRQP projection is informative. No certification, legal recognition, production security approval, universal interoperability or formal TRQP conformance is claimed.
