---
layout: default
title: "Agent Registry Protocol"
nav_exclude: true
---

# Agent Registry Protocol

[![Specification status](https://img.shields.io/badge/specification-v0.9.4%20historical--resolution-blue)](https://sankarshanmukhopadhyay.github.io/agent-registry-protocol/spec/agent-registry-protocol-v0.9.0.html)
[![Validation](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/actions/workflows/validate.yml/badge.svg)](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/actions/workflows/validate.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/spec-CC%20BY%204.0-lightgrey.svg)](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/blob/main/LICENSE-CONTENT)
[![Code: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-lightgrey.svg)](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/blob/main/LICENSE-CODE)

**A modular authority-control protocol for governed agent identity, delegation, recognition, lifecycle, evidence, enforcement and redress.**

> An agent registry is not merely a directory. It is an authority control plane whose claims must be scoped, revocable, inspectable and enforceable.

## Repository status

| Attribute | Value |
|---|---|
| Portfolio tier | Flagship |
| Maturity | Pilot ready |
| Lifecycle | Active |
| Operational status | Active validation |
| Specification status | Community Draft |
| Implementation release | v0.9.4 |
| Normative baseline | v0.9.0 Candidate Specification surface |
| Primary artifacts | Specification, schemas, API/event contracts, reference implementations, conformance and evidence |
| Release gate | `make release-check-all` |
| Candidate evidence | `artifacts/candidate-specification/evidence-bundle.json` |
| Authority | Member-owned status and scope in `PROJECT-STATUS.yaml`; process in `GOVERNANCE.md` |

## What v0.9.4 delivers

- deterministic historical authority resolution separating requested-time state from current state;
- explicit reconstruction quality, selected-record provenance, later material events, historical-effect and retention semantics;
- fifteen release-gated historical-resolution vectors with machine-readable evidence;
- portfolio-aligned `PROJECT-STATUS.yaml` with executable status/authority validation;
- A2A registry publication semantics separating portable Agent Cards, publication projections and authorization overlays;
- structured caller-visible discovery, exact Agent Card URI preservation and immutable snapshot/reference semantics;
- Agent Card compatibility classification and twelve additional registry-assurance vectors;
- an executable 15-minute path from clone to a resolved governed agent;
- a canonical sample registry, pilot kit and machine-readable readiness evidence;
- stable Candidate Specification requirements and conformance targets;
- hardened authority, delegation, recognition and fail-closed lifecycle semantics;
- two independently structured projection implementations with disclosed limits;
- network-boundary discovery and durable event replay, deduplication and acknowledgement tests;
- production-oriented proof, key and policy integration boundaries;
- machine-readable compatibility, requirement and evidence artifacts;
- an informative ARPA–TRQP governed query-projection profile with architecture guidance, mappings and 13 positive/negative vectors;
- flagship documentation, CI, GitHub Pages, contribution controls and AI-use governance.

## Start here

1. [Choose the correct journey in Start Here](docs/start-here.md)
2. [Run the 15-minute implementation quickstart](docs/implementation-accelerator/01-15-minute-quickstart.md)
3. [Implementation Accelerator](docs/implementation-accelerator/index.md)
4. [Documentation home](docs/index.md)
5. [Authoritative v0.9.0 Candidate Specification](https://sankarshanmukhopadhyay.github.io/agent-registry-protocol/spec/agent-registry-protocol-v0.9.0.html)
6. [Candidate implementation guide](docs/candidate-specification-guide.md)
7. [Historical Authority Resolution](docs/historical-authority-resolution.md)
8. [ARPA–TRQP interoperability architecture](docs/architecture/trqp-arpa-interoperability.md)
9. [Migration from v0.5.0](docs/migration-v0.5.0-to-v0.9.0.md)
10. [A2A Registry Integration Guide](docs/a2a-registry-integration-guide.md)
11. [TypeScript implementation track](docs/typescript-implementation.md)
12. [Known limitations](KNOWN_LIMITATIONS.md)

## Validate and produce evidence

```bash
make setup
make release-check-all
```

The full gate validates the complete Python release surface plus the TypeScript implementation track and Python↔TypeScript conformance equivalence evidence. The current released implementation remains v0.9.4; the TypeScript work is a v0.9.5 development track against that baseline.

## Development toward v0.9.5

The repository now includes an [independent TypeScript implementation track](docs/typescript-implementation.md) rooted in the v0.9.4 normative baseline. It independently implements the deterministic resolution and authority semantics exercised by the shared Profiles A–D vectors and emits machine-readable cross-runtime evidence. This repository-owned implementation diversity improves pre-v1.0 assurance but does not substitute for external organisational independence.

## ARPA and TRQP

ARPA owns the authority, lifecycle, evidence, revocation, enforcement and federation control plane. TRQP is treated as an external, minimal read-only query interface. The optional v0.9.0 projection demonstrates how selected ARPA authorization and recognition state can be exposed without merging the protocols or implying cross-protocol conformance.


## Licensing

ARPA uses **artifact-specific licensing** so that specification content and executable implementation artifacts have licenses suited to their use:

- **Specification and human-readable content:** [CC BY 4.0](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/blob/main/LICENSE-CONTENT)
- **Code and executable/machine-readable artifacts:** [Apache License 2.0](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/blob/main/LICENSE-CODE)

Machine-readable schemas, OpenAPI/AsyncAPI contracts, validators, test vectors, fixtures, mappings, executable configuration and generated machine-readable evidence are treated as software artifacts under Apache-2.0 unless a file explicitly states otherwise. Normative and informative specification prose, documentation, diagrams, governance prose, narrative examples and release notes are content under CC-BY-4.0.

See the repository [licensing map](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/blob/main/LICENSE), [NOTICE](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/blob/main/NOTICE), and machine-readable [artifact license policy](licensing/artifact-license-policy.json) for the deterministic classification rules.

## Assurance boundary

The supplied implementations and loopback network tests are repository-controlled candidate evidence, not external certification or proof of universal interoperability. The release does not claim legal authority, production key custody, formal cryptographic review, independent TRQP approval, or completed revocation without enforcement acknowledgement. See [known limitations](KNOWN_LIMITATIONS.md), [AI usage](AI_USAGE.md), [governance](GOVERNANCE.md), and [security](SECURITY.md).
