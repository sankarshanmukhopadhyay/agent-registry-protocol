---
layout: default
title: "ARPA v0.9.5 Release Notes"
nav_exclude: true
---

# ARPA v0.9.5 — TypeScript implementation and developer navigation

ARPA v0.9.5 adds an independently structured TypeScript implementation track and makes cross-runtime behaviour an executable release-gated assurance surface. The normative protocol baseline remains the v0.9.0 Candidate Specification; v0.9.5 adds implementation and interoperability evidence rather than a competing normative specification.

## Highlights

- TypeScript v0.3.0 implementation of deterministic resolution and authority semantics.
- Effective-time and historical-resolution reliance handling across the v0.9.4 historical corpus.
- Decision receipts, event continuity and fail-closed evidence handling.
- Thin Node.js HTTP registry surface and reusable `ArpaClient`.
- A2A publication and compatibility helpers that explicitly preserve the discovery-is-not-authority invariant.
- Python↔TypeScript deterministic and historical outcome equivalence.
- Bidirectional loopback HTTP interoperability, including TypeScript-client consumption of the Python registry.
- Task-oriented GitHub Pages information architecture: Understand, Build, Assure, Operate, Integrate and Govern.

## Assurance evidence

The release gate now includes:

```bash
make release-check-all
```

with TypeScript evidence under `artifacts/typescript/` for deterministic conformance, historical resolution, A2A adapters, cross-runtime equivalence and HTTP network interoperability.

## Developer experience

The documentation no longer requires developers to infer a reading order from a large flat catalogue. Existing URLs are retained, while six stable journey pages route users according to the decision they need to make. The exhaustive documentation catalogue remains available for reference.

## Compatibility and scope

The release does not alter the v0.9.0 Candidate Specification requirements. The TypeScript server is development-grade and uses in-memory persistence. Production key custody, cryptographic proof verification, issuer competence, distributed federation and externally independent implementation evidence remain outside the claimed release assurance boundary.
