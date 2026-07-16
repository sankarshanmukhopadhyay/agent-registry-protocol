# v0.5.0 Validation Summary

## Release gate

The release was validated on 16 July 2026 using:

```bash
make release-check
```

## Results

| Validation surface | Result |
|---|---:|
| Valid and invalid schema examples | 44/44 passed |
| Profile conformance vectors | 12/12 passed |
| Extended governance vectors | 14/14 passed |
| Schema, controlled-registry, OpenAPI, and AsyncAPI parsing | Passed |
| Flagship repository baseline and local Markdown links | Passed |
| Reference-service tests | 5/5 passed |
| Interoperability gates | 7/7 passed |
| Reference implementation report | Passed |

## Evidence produced

- `conformance/reports/reference-implementation-report.json`
- `artifacts/interoperability/interoperability-report.json`
- `artifacts/interoperability/evidence-bundle.json`

## Assurance boundary

These results demonstrate reproducibility of the repository artifacts and supplied fixtures. They do not constitute independent implementation evidence, production security assurance, legal recognition, or certification.
