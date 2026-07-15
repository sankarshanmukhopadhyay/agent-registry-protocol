# v0.4.0 Validation Summary

## Automated results

| Surface | Result |
|---|---:|
| Valid and targeted invalid schema examples | 44/44 passed |
| Profile A-D decision vectors | 12/12 passed |
| Extended governance and interoperability vectors | 14/14 passed |
| Reference service integration tests | 4/4 passed |
| JSON Schema meta-validation | Passed |
| Controlled registry uniqueness and structure | Passed |
| OpenAPI and AsyncAPI YAML parsing | Passed |
| Machine-readable implementation report | Generated; all checks passed |

## Evidence produced

- `conformance/reports/reference-implementation-report.json`
- positive and negative records under `examples/`
- profile vectors under `conformance/test-vectors/TV-*`
- governance vectors under `conformance/test-vectors/extended/`
- FastAPI integration tests under `reference/tests/`

## Assurance boundary

The results establish deterministic behavior for the published schemas, vectors and local reference service. They do not establish production security, legal authority, regulatory certification, independent interoperability or operational service-level compliance. See `KNOWN_LIMITATIONS.md`.
