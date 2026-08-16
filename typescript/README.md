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

The v0.1.0 track provides:

- canonical identifier-resolution outcomes;
- deterministic authority evaluation for the pure §28.2 semantics covered by Profiles B-D vectors;
- fail-closed status, scope, expiry, prohibition, limit and approval handling;
- direct schema and registry catalog consumption;
- execution of the shared conformance corpus;
- machine-readable TypeScript conformance evidence.

It intentionally does not claim production federation, proof verification, key custody, issuer competence resolution, persistence or external independent-operation evidence.

## Development

```bash
npm install
npm run release-check
```

The conformance report is written to `../artifacts/typescript/conformance-report.json`.

## Governance invariant

Discovery, registration or successful resolution MUST NOT be interpreted as authority. `Profile A` authority evaluation is therefore explicitly `not_applicable`.
