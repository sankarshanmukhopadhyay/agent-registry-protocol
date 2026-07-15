# Agent Registry Protocol

[![Specification status](https://img.shields.io/badge/specification-v0.4.0%20community%20draft-blue)](spec/draft-agent-registry-protocol-architecture.md)
[![Validation](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/actions/workflows/validate.yml/badge.svg)](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/actions/workflows/validate.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/spec-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![Code: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-lightgrey.svg)](LICENSE-CODE)

**A modular protocol for treating agent registries as distributed authority-control planes for delegated action.**

> An agent registry is not merely a directory of autonomous software objects. It is infrastructure for resolving identity, attribution, bounded authority, assurance, status, evidence, governance and redress without collapsing those claims into a universal trust flag.

## v0.4.0 deliverables

- six composable protocol modules and a minimal ARPA-Core profile;
- canonical `agentreg` identifiers and governed aliases;
- 20 normative record schemas plus Agent Card and registry metadata schemas;
- machine-readable controlled registries;
- OpenAPI and AsyncAPI contracts;
- typed relationship and issuer-competence semantics;
- multidimensional conformance reports;
- a runnable FastAPI/SQLite reference registry, resolver, event service and PDP;
- end-to-end adoption scenarios, deployment guidance and hardened CI.

## Start here

1. [Architecture specification](spec/draft-agent-registry-protocol-architecture.md)
2. [Protocol modules](docs/protocol-modules.md)
3. [Implementation selection guide](docs/implementation-selection-guide.md)
4. [ARPA-Core profile](spec/profiles/arpa-core-identity-discovery-profile.md)
5. [Quickstart](docs/quickstart.md)
6. [OpenAPI contract](openapi/arpa-openapi.yaml)
7. [Conformance guide](docs/conformance-guide.md)
8. [Known limitations](KNOWN_LIMITATIONS.md)

## Validate and run

```bash
make setup
make validate
make test
make report
make run
```

API documentation is available at `http://127.0.0.1:8000/docs` while the reference service is running.

## Repository structure

```text
spec/          architecture and normative profiles
docs/          implementor, operator, security and governance guidance
schemas/       JSON Schema 2020-12 record contracts
registries/    controlled machine-readable identifiers
openapi/       REST contract
asyncapi/      event contract
reference/     runnable reference registry, resolver and PDP
conformance/   profiles, vectors and implementation reports
examples/      valid/invalid records and end-to-end scenarios
scripts/       validators and report generation
```

## Governing distinctions

Identity is not authority. Key control is not accountability. Capability is not permission. Ownership is not delegation. Assurance is not universal trust. Registry revocation is incomplete until enforcement surfaces converge. Technical federation does not imply governance recognition.

## Status and licensing

This is an independent community draft, not an adopted standard. Specifications and documentation use CC BY 4.0; code and executable artifacts use Apache-2.0. See [LICENSE](LICENSE), [LICENSE-CODE](LICENSE-CODE) and [NOTICE](NOTICE).
