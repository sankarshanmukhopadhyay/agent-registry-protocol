---
layout: default
title: "Release Notes v0.9.3"
nav_exclude: true
---

# Agent Registry Protocol v0.9.3 — A2A Registry Convergence & Publication Semantics

ARPA v0.9.3 aligns the A2A interoperability profile with the emerging Agent Card / Publication Record / Authorization Overlay registry model while retaining the v0.9.0 Candidate Specification as the normative protocol baseline.

## Highlights

- Formalizes the separation between portable **Agent Cards**, registry **Publication Projections**, and caller-specific **Authorization Overlays**.
- Adds a machine-readable A2A publication projection schema without creating a second authoritative ARPA record type.
- Adds auth-context-scoped structured `GET /agents` discovery semantics.
- Preserves the exact publisher-supplied Agent Card URI and digest-bound observation metadata.
- Defines list/search, resolve, and immutable snapshot/reference semantics for replayable decisions.
- Adds an Agent Card compatibility result model with `compatible`, `breaking`, and `indeterminate` classifications.
- Adds twelve registry-specific positive and negative assurance vectors in addition to the existing A2A task/card vectors.
- Produces dedicated A2A registry interoperability reports and evidence bundles in the release gate.

## Governance boundary

**Discoverability is not authority. Publication is not delegation. Endpoint authentication is not permission to act.**

A successful listing, card resolution, card signature check, endpoint authentication, task acceptance, or task completion does not establish delegated authority, principal consent, capability verification, issuer competence, assurance, governance recognition, or legal permission. Authoritative ARPA suspension, revocation, delegation expiry and recognition withdrawal continue to take precedence over published Agent Card content.

## Registry interoperability posture

The release deliberately does **not** mandate a federation topology or registry substrate. Centralized enterprise catalogs, federated catalogs, peer registries, xRegistry adapters, SPIFFE/mTLS, OpenID Federation, DCAT/JSON-LD, DID-based identifiers and advanced vector/graph search can be layered on without changing ARPA's publication/authority separation.

## Compatibility semantics

The repository classifier treats additions of advertised functionality as compatible unless they narrow prior behavior. Removing previously advertised skills, interfaces, security schemes, supported input/output modes, or disabling a previously available capability is breaking. Unknown changes are indeterminate and require local policy.

Compatibility classification is change-management evidence only; it does not prove capability, safety, or authority.

## Compatibility

- **Normative ARPA specification:** v0.9.0 Candidate Specification
- **Implementation release:** v0.9.3
- **A2A interoperability profile:** A2A protocol family 1.0, registry-aligned revision
- Existing ARPA-Core record schemas remain compatible.
- The publication projection is additive and derived from existing records.
- A2A support remains optional for ARPA-Core conformance.

## Validation

```bash
python3 scripts/validate_a2a_interoperability.py
make release-check
```

The release gate validates exact Agent Card URI preservation, visibility filtering, snapshot retention, Agent Card compatibility classification, ARPA authority precedence, and non-implication of authority from discovery or endpoint authentication.

Passing repository-controlled vectors demonstrates conformity of the supplied implementation artifacts only. It is not certification, legal recognition, production deployment assurance, or independent A2A interoperability validation.
