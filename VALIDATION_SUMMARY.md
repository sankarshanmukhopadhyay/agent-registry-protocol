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
