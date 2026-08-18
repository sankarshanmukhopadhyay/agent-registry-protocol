---
layout: default
title: "Agent Registry Protocol"
nav_exclude: true
---

# Agent Registry Protocol

[![Specification status](https://img.shields.io/badge/implementation-v0.9.5%20cross--runtime-blue)](https://sankarshanmukhopadhyay.github.io/agent-registry-protocol/spec/agent-registry-protocol-v0.9.0.html)
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
| Implementation release | v0.9.5 |
| Normative baseline | v0.9.0 Candidate Specification surface |
| Primary artifacts | Specification, schemas, API/event contracts, reference implementations, conformance and evidence |
| Release gate | `make release-check-all` |
| Candidate evidence | `artifacts/candidate-specification/evidence-bundle.json` |
| Authority | Member-owned status and scope in `PROJECT-STATUS.yaml`; process in `GOVERNANCE.md` |

## What v0.9.5 delivers

- an independent TypeScript v0.3.0 implementation track over shared normative artifacts;
- 27/27 Python↔TypeScript deterministic and historical outcome-equivalence checks;
- a thin TypeScript HTTP service, reusable `ArpaClient`, and 7/7 network interoperability checks;
- A2A publication/compatibility adapters with explicit discovery-is-not-authority semantics;
- a task-oriented documentation architecture organized around Understand, Build, Assure, Operate, Integrate, and Govern;
- deterministic historical authority resolution separating requested-time state from current state;
- explicit reconstruction quality, selected-record provenance, later material events, historical-effect and retention semantics;
- fifteen release-gated historical-resolution vectors with machine-readable evidence;
- eight release-gated governance/privacy assurance vectors covering administrative capture, revocation convergence, federation conflict, restricted discovery and compromise restoration;
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

## IETF Internet-Draft track

ARPA now maintains a deliberately separate IETF authoring surface for the protocol core. The initial individual-draft series is **`draft-sankarshan-agent-registry-protocol`**. It does not replace the ARPA Candidate Specification or reuse ARPA semantic-version numbers.

- [IETF authoring and submission guide](ietf/)
- [Protocol extraction map](ietf/PROTOCOL_EXTRACTION.md)
- [`-00` submission checklist](ietf/SUBMISSION_CHECKLIST.md)
- [Internet-Draft source](ietf/draft-sankarshan-agent-registry-protocol.md)

Build and validate the draft with `make ietf-setup` followed by `make ietf-check`. The IETF source is prepared as a prospective IETF Contribution; existing ARPA artifact-specific licensing remains unchanged.

## Start here

Choose the path that matches the decision you need to make:

- [Understand ARPA](docs/understand.md) — concepts, modules and non-implication rules.
- [Build ARPA](docs/build.md) — implementation paths, machine-readable artifacts and developer quickstarts.
- [Assure & Conform](docs/assure.md) — profiles, release gates and evidence.
- [Operate ARPA](docs/operate.md) — deployment, governance, security, privacy and lifecycle operations.
- [Integrate & Interoperate](docs/integrate.md) — A2A, TRQP and cross-runtime integration.
- [Govern & Contribute](docs/govern.md) — change control, releases and repository governance.

Use [Start Here](docs/start-here.md) for the decision router or the [documentation catalogue](docs/index.md) for the complete rendered surface.

## Validate and produce evidence

```bash
make setup
make release-check-all
```

The full gate validates the Python release surface, TypeScript conformance and historical semantics, A2A adapters, same-corpus Python↔TypeScript equivalence, and loopback HTTP network interoperability.

## TypeScript and cross-runtime assurance

The [TypeScript implementation](docs/typescript-implementation.md) independently implements the supported ARPA semantics, exposes a development HTTP/client surface, and emits deterministic, historical, A2A and network interoperability evidence. Repository-owned implementation diversity improves pre-v1.0 assurance but does not substitute for externally operated independent implementation evidence.

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
