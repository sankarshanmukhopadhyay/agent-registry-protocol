---
layout: default
title: "JSON Schemas"
nav_exclude: true
---

# JSON Schemas

ARPA Candidate Specification v0.9.0 publishes JSON Schema 2020-12 contracts for the record families and standalone interoperability/evidence artifacts under this directory. The core record schema track remains `1.0.0`; implementation releases v0.9.1–v0.9.5 continue to consume the v0.9.0 Candidate normative baseline.

Every envelope-based record composes `common/envelope.schema.json`. Valid and targeted invalid examples are under `examples/`; `scripts/validate_examples.py` resolves local references and validates expected outcomes.

## Version mapping

| ARPA document | Record schema track |
|---|---|
| 0.3.0 | 1.0.0 |
| 0.5.0 | 1.0.0 |
| 0.9.0 Candidate | 1.0.0 |
| 0.9.1–0.9.5 implementation releases | 1.0.0 (v0.9.0 Candidate baseline) |

A required-field or semantic change requires coordinated document, schema, example, vector and migration updates. Editorial changes do not require a schema-version bump.


### v0.9.3 A2A registry interoperability

- `a2a-publication-projection.schema.json` — derived registry publication/search projection; not an authoritative identity or authority record.
- `a2a-card-compatibility-result.schema.json` — machine-readable compatibility classification for successive Agent Card representations.

- `historical-resolution.schema.json` — requested-time/current-state historical authority resolution with evidence provenance.

- `project-status.schema.json` — repository-local compatibility snapshot of the portfolio member status contract; upstream governance retains authority.
