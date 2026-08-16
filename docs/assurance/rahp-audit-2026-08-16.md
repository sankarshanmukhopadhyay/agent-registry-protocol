---
layout: default
title: "RAHP Audit — 2026-08-16"
nav_exclude: true
---

# ARPA full RAHP audit — 2026-08-16

## Executive assessment

ARPA v0.9.5 was assessed in **combined RAHP + security-hardening mode** using the uploaded RAHP Toolkit v1.0.0 corpus and engine contract. The audit covered the normative v0.9.0 Candidate Specification, schemas, controlled registries, API/event contracts, Python and TypeScript reference implementations, conformance vectors, governance, security/privacy guidance, historical resolution, A2A integration, TRQP projection, and release evidence.

The baseline was already strong. ARPA explicitly separates discovery from authority, scopes delegation, requires fail-safe handling of stale/conflicting authority, models revocation convergence, preserves historical state, prevents transitive federation assumptions, and treats redress as part of the protocol control loop. The material findings were therefore **assurance-depth gaps rather than architectural omissions**: controls against administrative capture, privacy-invasive discovery, incomplete revocation convergence, federation conflict, weak recovery, and under-specified due process were not all equally normative or release-gated.

This commit closes all repository-addressable findings identified in the audit. Residual items are deployment-assurance obligations that cannot be proven by repository code alone.

## Audit provenance

| Field | Value |
|---|---|
| Audit ID | `ARPA-RAHP-2026-08-16` |
| Mode | Combined RAHP + security hardening |
| RAHP Toolkit | v1.0.0 / `rahp-engine-contract-v1` |
| ARPA implementation release | v0.9.5 |
| Normative baseline | v0.9.0 Candidate Specification |
| ARPA archive SHA-256 | `192d34182d5b5cdcea8b7d27fd9cde1cb9c730e7bd029d8edba5dd309fdc3ec6` |
| RAHP archive SHA-256 | `ad98f39f45dc96bc3dc8e7688c4b8e4756525aaa45a21be49fdc3aed894bc4a5` |
| Machine-readable audit | `artifacts/governance-assurance/rahp-audit-2026-08-16.yaml` |

## Findings and dispositions

| Finding | Severity | Audit conclusion | Repository remediation | Evidence |
|---|---|---|---|---|
| High-impact registry administration insufficiently protected from governance capture | High / Critical security path | Threshold control existed, but was advisory and concentrated in high-assurance guidance. | Profile C/D high-impact administration now requires threshold, dual-control, or equivalent independent authorization. | `GA-01`, `GA-02` |
| Consequential lifecycle actions lacked a complete normative due-process floor | High | Appeal existed, while notice, evidence standards, emergency exception handling, decision authority and remedy mechanics remained advisory. | Profile B-D consequential lifecycle governance now has mandatory minimum due-process and resolvable redress requirements. | Specification §§27.4–27.5 |
| Discovery and graph publication could enable aggregation/correlation harms | High | Privacy architecture recognized the risk, but higher-profile query controls and relationship disclosure classification were advisory. | Non-public queries are policy-bound; unauthenticated discovery is public-only; sensitive relationship disclosure classification is mandatory. | `GA-07` |
| Revocation could be semantically correct but operationally unconverged | High | ARPA already requires enforcement acknowledgement but had no dedicated negative control vector for partial acknowledgement. | Added explicit incomplete/complete convergence vectors and evidence generation. | `GA-03`, `GA-04` |
| Federation conflict/withdrawal could regress without targeted negative tests | High | Recognition was non-transitive and withdrawable, but conflict handling had no dedicated release-gated suite. | Unresolved conflicts are explicitly non-affirmative; withdrawal and conflict vectors added. | `GA-05`, `GA-06` |
| Compromise recovery remained a high-value governance attack path | High / Critical security path | Recovery abuse was in the threat model, but restoration assurance was not independently release-gated. | Restoration after confirmed compromise is covered by independent multi-party authorization and fresh security evidence. | `GA-08` |

## Positive controls credited by the audit

The audit expressly credits existing ARPA controls rather than treating every threat as a gap: capability and discovery do not imply authority; delegation must narrow at every hop; proof validity does not imply authority validity; stale/conflicting/unavailable authority is non-affirmative; technical federation does not imply recognition; recognition is scoped and withdrawable; revocation requires enforcement acknowledgement; historical resolution distinguishes requested-time from current state; execution/decision receipts preserve policy and evidence context; and profile claims are evidence-bounded.

## New executable assurance surface

The new `arpa-governance-assurance-v1` suite contains eight deterministic vectors:

- `GA-01` — valid independent authorization for a high-impact administrative change;
- `GA-02` — rejection of unilateral compromise restoration;
- `GA-03` — incomplete revocation acknowledgement is not converged;
- `GA-04` — full required acknowledgement is converged;
- `GA-05` — unresolved federation status conflict is indeterminate;
- `GA-06` — withdrawn recognition is non-affirmative;
- `GA-07` — unauthenticated discovery filters private/tenant records; and
- `GA-08` — compromise restoration requires fresh evidence and independent authorization.

Run `python3 scripts/validate_governance_assurance.py`. The suite is included in `make validate` and produces `artifacts/governance-assurance/evidence-bundle.json`.

## Residual assurance boundary

The repository cannot by itself prove production operator separation, secure key custody, real multi-party administration, cross-operator federation behavior, heterogeneous enforcement acknowledgement, accessible legal redress, or deployment-specific privacy compliance. These remain explicit deployment and independent-assurance obligations rather than hidden assumptions.

## Retest triggers

Re-run the combined RAHP audit when ARPA changes administrative authority, recovery, revocation, discovery/listing, federation/recognition, redress, privacy disclosure, conformance profiles, or the semantics of `allow`/`indeterminate` decisions. A v1.0 readiness review should additionally require independently operated evidence for at least one Profile C or D deployment.
