---
layout: default
title: "Governance and Security Assurance"
nav_exclude: true
---

# Governance and Security Assurance

This profile turns the highest-priority governance and privacy findings from the 2026-08-16 RAHP review into executable release controls. It complements, rather than replaces, the core protocol, security deployment guidance, and profile conformance vectors.

## Control objectives

| Control | Required property | Evidence |
|---|---|---|
| High-impact administration | Profile C/D changes to accountable entities, recovery, governance, broad authority, critical prohibitions and evidence deletion require independent multi-party authorization. | `GA-01`, `GA-02` |
| Revocation convergence | Revocation is not reported as converged until every enforcement point required by policy has acknowledged the change. | `GA-03`, `GA-04` |
| Federation recognition | Withdrawal is fail-closed and unresolved source conflicts are non-affirmative. | `GA-05`, `GA-06` |
| Discovery privacy | Unauthenticated discovery cannot expose records classified as private or tenant-specific. | `GA-07` |
| Recovery after compromise | Restoration after confirmed compromise requires fresh security evidence and independent multi-party authorization. | `GA-08` |

## Run the assurance suite

```bash
python3 scripts/validate_governance_assurance.py
```

The validator emits `artifacts/governance-assurance/evidence-bundle.json`. It is also included in `make validate` and therefore in the release gate.

## Assurance boundary

These vectors demonstrate that the repository's declared control semantics are internally testable. They do not prove that a production operator has implemented independent approvers, secure key custody, privacy-preserving query infrastructure, external enforcement acknowledgements, or a legally sufficient redress process. Those claims require deployment evidence and accountable sign-off.
