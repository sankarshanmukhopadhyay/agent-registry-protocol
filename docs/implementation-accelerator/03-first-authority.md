---
layout: default
title: "Your first authority"
parent: "Implementation Accelerator"
nav_order: 3
---
# Your first authority

ARPA distinguishes registration from authority. Registration answers **what agent record exists**. Authority answers **who may cause which action, for which purpose, within what scope and until when**.

The Acme sample uses an accountable organisation, a delegated registrar relationship and a governed procurement-review agent. The authority envelope in `implementation-accelerator/fixtures/acme/authority-envelope.json` binds the issuer, subject, scope, validity and proof placeholder.

## Testable outcome

Post `implementation-accelerator/requests/authority-allow.json` to `/authority/evaluate`. Retain the returned decision receipt as evidence of the evaluator, policy version, request digest, decision and reason codes.

A pilot must also exercise `authority-deny.json` and prove that an out-of-scope action fails closed.
