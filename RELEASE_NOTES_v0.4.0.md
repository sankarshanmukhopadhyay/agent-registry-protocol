---
layout: default
title: "ARPA v0.4.0: Protocol Contracts and Reference Implementation Release"
nav_exclude: true
---

# ARPA v0.4.0: Protocol Contracts and Reference Implementation Release

ARPA v0.4.0 turns the architecture draft into a modular, machine-verifiable implementation package while preserving the central distinction between identity, authority, assurance, accountability and governance.

## Highlights

The release introduces six composable modules: ARPA-Core, Relations, Assurance, Authority, Evidence and Federation. Profile A can now be implemented independently as a real identity and discovery registry, while unsupported higher-layer functions must return deterministic non-support responses rather than implied trust or authority.

The release adds a canonical identifier and governed alias profile, completed record schemas, controlled protocol registries, an OpenAPI REST contract, an AsyncAPI event contract, a generic Agent Card interoperability profile, typed issuer-competence and transfer semantics, and multidimensional conformance reporting.

A runnable FastAPI and SQLite reference service demonstrates registration, non-reassignable identifiers, resolution, point-in-time filtering, alias conflict handling, append-only event replay, authority evaluation and decision receipts. Docker, Compose, Make targets and CI provide a reproducible adoption path.

## Validation

- 44/44 valid and invalid schema examples passed.
- 12/12 Profile A-D decision vectors passed.
- 14/14 extended governance and interoperability vectors passed.
- 4/4 reference service integration tests passed.
- OpenAPI, AsyncAPI, schemas and controlled registries passed structural validation.

## Security and governance

The release explicitly covers alias hijacking, issuer confusion, unauthorized control changes, projection poisoning, stale status, event gaps, transfer abuse, authority expansion and revocation-convergence failure. Registration, ownership-like control and metadata integrity remain non-equivalent to delegated authority or assurance.

## Known limitations

The reference implementation is not production-ready. It does not provide production key custody, distributed consensus, independent identity proofing, universal policy execution, production federation or regulatory certification. Independent interoperability testing remains the next maturity gate.
