# JSON Schemas

ARPA v0.5.0 publishes JSON Schema 2020-12 contracts for 20 envelope-based record families plus standalone Agent Card extension and Registry Metadata contracts. The record schema track remains `1.0.0`.

Every envelope-based record composes `common/envelope.schema.json`. Valid and targeted invalid examples are under `examples/`; `scripts/validate_examples.py` resolves local references and validates expected outcomes.

## Version mapping

| ARPA document | Record schema track |
|---|---|
| 0.3.0 | 1.0.0 |
| 0.5.0 | 1.0.0 |

A required-field or semantic change requires coordinated document, schema, example, vector and migration updates. Editorial changes do not require a schema-version bump.
