---
layout: default
title: "Release Notes v0.9.4"
nav_exclude: true
---

# ARPA v0.9.4 — Historical Authority Resolution and Governance Alignment

ARPA v0.9.4 turns the protocol's existing time-dependent lifecycle and event model into an explicit, machine-verifiable historical authority-resolution capability while aligning repository governance with the portfolio's federated status contract.

## Highlights

- Adds `PROJECT-STATUS.yaml` as the member-owned source for maturity, lifecycle, operational status, specification status, authority scope, validation, evidence, and explicit non-claims.
- Defines deterministic historical resolution that separates requested-time state from current state.
- Adds explicit reconstruction quality, selected-record provenance, later material events, historical-effect semantics, retention status, and evidence-integrity status.
- Clarifies prospective, retroactive, governance-defined, and indeterminate effects of later revocation, compromise, supersession, or recognition withdrawal.
- Preserves the boundary between registry-resolved historical authority and relying-party acceptance policy.
- Adds a machine-readable historical-resolution schema and controlled vocabularies.
- Adds fifteen positive/negative historical-resolution vectors and a release-gated validator producing `artifacts/historical-resolution/evidence-bundle.json`.
- Strengthens ARPA–TRQP guidance for as-of query projection while keeping TRQP an external, non-normative dependency.

## Governance alignment

The repository status contract is aligned with the governed portfolio declaration:

- maturity: `pilot-ready`
- lifecycle: `active`
- operational status: `active-validation`
- specification status: `community-draft`
- portfolio tier: `flagship` (portfolio-owned declaration)

ARPA owns its protocol, record model, lifecycle semantics, profiles, and evidence requirements. It does not claim ownership of TRQP, A2A, relying-party policy, legal recognition, or certification.

## Historical-resolution invariants

- Historical state MUST NOT be replaced by current state.
- Later material events MUST be disclosed when relevant to interpretation.
- Retroactive effect MUST be grounded in an applicable governance rule or authoritative event declaration.
- Missing, conflicting, withheld, or integrity-failed evidence MUST produce a bounded non-affirmative reconstruction outcome.
- Historical validity does not compel relying-party acceptance.

## Interoperability context

The capability is intentionally aligned with lifecycle and historical/as-of verification concerns discussed in ToIP TRQP issue #176 and UN/CEFACT GTR issue #75. Neither external project becomes a normative dependency, and ARPA conformance does not imply conformance to either external specification.

## Validation

Release validation includes:

```bash
make release-check
make pages-check
```

The historical-resolution gate validates fifteen vectors and produces a machine-readable evidence bundle under `artifacts/historical-resolution/`.

## Assurance boundary

This release provides repository-controlled conformance evidence. It does not constitute external certification, legal determination, formal standards adoption, or independent assurance.
