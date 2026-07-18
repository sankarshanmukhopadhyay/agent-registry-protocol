---
layout: default
title: "Validation Summary — ARPA v0.9.0"
nav_exclude: true
---

# Validation Summary — ARPA v0.9.0

Validation command:

```bash
make release-check
```

## Results

| Surface | Result |
|---|---:|
| Valid and invalid schema examples | 44/44 passed |
| Profile conformance vectors | 12/12 passed |
| Extended governance vectors | 14/14 passed |
| Reference-service tests | 5/5 passed |
| v0.5-derived interoperability checks updated for v0.9.0 | 7/7 passed |
| ARPA–TRQP projection vectors and candidate checks | 15/15 passed |
| Candidate mapping completeness | Passed |
| Schemas, controlled registries, OpenAPI and AsyncAPI parsing | Passed |
| Flagship repository artifacts and local Markdown links | Passed |
| Implementation report generation | Passed |

## Retained evidence

- `artifacts/candidate-specification/candidate-validation-report.json`
- `artifacts/candidate-specification/evidence-bundle.json`
- `artifacts/candidate-specification/requirements.json`
- `artifacts/interoperability/interoperability-report.json`
- `artifacts/interoperability/evidence-bundle.json`
- `artifacts/release/compatibility-matrix.json`
- `conformance/reports/reference-implementation-report.json`

## Assurance boundary

The bundled implementation paths are maintained in one repository and are not evidence of independent external adoption. Network testing uses loopback endpoints, durable-event behavior uses SQLite, and the ARPA–TRQP profile is informative. The validation does not constitute certification, legal recognition, formal TRQP conformance, production security approval, or universal interoperability.

## Specification authority correction

The release now has one authoritative prose specification:
`spec/agent-registry-protocol-v0.9.0.md`. The unchanged v0.5.0 draft and
detached Candidate requirements overlay have been removed. All repository
references and validation gates resolve to the consolidated specification.

## GitHub Pages publication hardening

The repository now declares 70 rendered Markdown sources in `docs/publication-map.yml`. The publication pipeline generates a deterministic source-to-output manifest and blocks deployment when a declared page is absent, an internal `.md` URL remains unresolved, a local target or asset is missing, a heading fragment is invalid, or two sources collide on one output path.

Offline validation completed for the publication inventory, explicit front matter, local Markdown source links, workflow YAML, repository validation, candidate validation, and the complete release-check suite. The authoritative Jekyll rendering check runs in GitHub Actions through `make pages-check`, where the pinned Ruby dependencies are installed by `ruby/setup-ruby`.

## v0.9.1 Implementation Accelerator validation

- `make release-check`: passed.
- Python service and publication-validator tests: 10 passed.
- End-to-end sample registry loading: 6 records accepted.
- Pilot readiness validator: 14/14 checks passed; decision `ready`.
- Publication manifest: 89 rendered pages declared.
- Local Jekyll rendering was not executed in the build environment because Bundler was unavailable; GitHub Actions remains the authoritative Pages rendering gate.

Passing these checks demonstrates repository-controlled reference behaviour only. It does not replace operator governance, security review, production hardening or independent conformance assessment.
