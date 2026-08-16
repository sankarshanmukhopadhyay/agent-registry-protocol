# ARPA TypeScript implementation track

This directory contains an **independent TypeScript interpretation** of the ARPA v0.9.4 protocol surface. It exists to improve implementation portability, interoperability evidence and pre-v1.0 specification assurance. It is not a line-by-line port of the Python reference service.

## Independence rule

TypeScript code consumes the normative repository artifacts directly:

- `../schemas/` for JSON Schema definitions;
- `../registries/` for governed code registries;
- `../conformance/test-vectors/` for observable protocol outcomes;
- the normative specification for behavioural requirements.

Behavioral code MUST NOT import, execute or mechanically translate `../reference/` or `../scripts/reference_evaluator.py`. Agreement between the Python and TypeScript implementations is evidence; shared implementation logic would weaken that evidence.

## Current milestone

The v0.2.0 track provides:

- canonical identifier-resolution outcomes;
- deterministic authority evaluation for the pure §28.2 semantics covered by Profiles B-D vectors;
- fail-closed status, scope, expiry, prohibition, limit and approval handling;
- direct schema and registry catalog consumption;
- execution of the shared conformance corpus;
- machine-readable TypeScript conformance evidence;
- effective-time record selection and historical-resolution reliance semantics;
- fail-closed retention and historical-evidence integrity handling;
- deterministic decision-receipt generation with request digests and evidence references;
- event-stream continuity checks and checkpoint reporting;
- 15-vector historical-resolution evidence alongside the shared Profile A-D corpus.

It intentionally does not claim production federation, proof verification, key custody, issuer competence resolution, persistence or external independent-operation evidence.

## Development

```bash
npm install
npm run release-check
```

Reports are written under `../artifacts/typescript/`, including `conformance-report.json`, `historical-resolution-report.json`, `implementation-report.json`, and `cross-runtime-report.json`.

## Governance invariant

Discovery, registration or successful resolution MUST NOT be interpreted as authority. `Profile A` authority evaluation is therefore explicitly `not_applicable`.
