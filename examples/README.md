# Examples

Machine-validatable example records, one valid and one invalid instance per record family defined in `schemas/`.

## Layout

```text
examples/
├── valid/     one instance per record family; each MUST validate cleanly
└── invalid/   one instance per record family; each MUST fail validation
```

Every `examples/invalid/<name>.json` file carries a `_violation` field (ignored by the schema — it is not schema-restricted via `additionalProperties`) that names the specific spec requirement it breaks, so the negative case is reviewable by a human without re-deriving why it fails.

## Validating

```bash
python3 ../scripts/validate_examples.py
```

This checks that every `valid/` file validates and every `invalid/` file does not, against the schema in `../schemas/<name>.schema.json` with the matching filename stem.

## Scenario coverage

The `valid/agent-core.json`, `valid/relationship.json`, `valid/authority-envelope.json`, and `valid/assurance-claim.json` examples are drawn from the specification's own Appendix A (with digests corrected to well-formed `sha256:` values), so the spec's illustrative examples and this directory's machine-validated examples stay in lockstep. The remaining ten record families' examples were newly authored for this directory following the same `agentreg:example.org:agent-123` procurement scenario used throughout spec §4.3 and Appendix A–C, so cross-references between files (e.g. `deployment_id`, `authority_envelope_id`) resolve consistently across the set.

## Planned end-to-end scenarios

The full set of end-to-end use-case walkthroughs originally scoped for this directory — covering each of the twelve use cases in spec §4 as a complete record sequence (registration → delegation → execution → revocation → appeal) rather than one record per family — remains open and is tracked in `ROADMAP.md` Phase 5 alongside the reference implementation. `conformance/test-vectors/` currently covers the decision-outcome slice of these scenarios (see `conformance/README.md`).
