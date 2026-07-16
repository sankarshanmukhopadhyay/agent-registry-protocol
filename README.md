# Agent Registry Protocol

[![Specification status](https://img.shields.io/badge/specification-v0.5.0%20interoperability%20draft-blue)](spec/draft-agent-registry-protocol-architecture.md)
[![Validation](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/actions/workflows/validate.yml/badge.svg)](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/actions/workflows/validate.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/spec-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![Code: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-lightgrey.svg)](LICENSE-CODE)

**A modular protocol for treating agent registries as distributed authority-control planes for delegated action.**

> An agent registry is not merely a directory of autonomous software objects. It resolves identity, attribution, bounded authority, assurance, status, evidence, governance, enforcement, and redress without collapsing those claims into a universal trust flag.

## Repository status

| Attribute | Value |
|---|---|
| Portfolio tier | Flagship candidate |
| Lifecycle | Active |
| Stability | v0.5.0 interoperability draft |
| Primary artifacts | Specification, schemas, controlled registries, API contracts, reference service, conformance and interoperability evidence |
| Release gate | `make release-check` |
| Evidence output | `artifacts/interoperability/evidence-bundle.json` |
| Authority | Community draft governed by `GOVERNANCE.md` |

## What v0.5.0 delivers

- six composable protocol modules and profile-specific conformance;
- canonical `agentreg` identifiers, governed aliases, and scoped registry recognition;
- 20 normative record schemas plus Agent Card and registry metadata schemas;
- controlled registries, OpenAPI and AsyncAPI contracts;
- runnable FastAPI/SQLite registry, resolver, event service, and policy decision point;
- positive, negative, and extended governance vectors;
- a two-registry interoperability harness covering discovery, resolution, recognition, event continuity, revocation, enforcement acknowledgement, and policy portability;
- machine-readable implementation reports and an interoperability evidence bundle;
- adoption, deployment, security, privacy, governance, migration, and AI-use guidance.

## Start here

1. [Documentation home](docs/index.md)
2. [Architecture specification](spec/draft-agent-registry-protocol-architecture.md)
3. [Quickstart](docs/quickstart.md)
4. [Interoperability guide](docs/interoperability.md)
5. [Implementation selection guide](docs/implementation-selection-guide.md)
6. [Conformance guide](docs/conformance-guide.md)
7. [Known limitations](KNOWN_LIMITATIONS.md)

## Validate, test, and produce evidence

```bash
make setup
make release-check
make run
```

`make release-check` validates schemas, examples, conformance vectors, repository controls, service tests, interoperability behavior, and implementation reporting. API documentation is available at `http://127.0.0.1:8000/docs` while the reference service runs.

## Governing distinctions

Identity is not authority. Key control is not accountability. Capability is not permission. Ownership is not delegation. Assurance is not universal trust. Technical federation is not governance recognition. Revocation is incomplete until enforcement surfaces acknowledge and apply it.

## Authority and limitations

This repository defines an independent community draft and its supplied implementation artifacts. It does not certify implementations, establish legal authority, provide production identity proofing, or count its own fixtures as independent implementations. Specifications and documentation use CC BY 4.0; code and executable artifacts use Apache-2.0. See [AI usage](AI_USAGE.md), [governance](GOVERNANCE.md), [security](SECURITY.md), and [release policy](docs/release-policy.md).
