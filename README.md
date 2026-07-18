---
layout: default
title: "Agent Registry Protocol"
nav_exclude: true
---

# Agent Registry Protocol

[![Specification status](https://img.shields.io/badge/specification-v0.9.1%20accelerator-blue)](https://sankarshanmukhopadhyay.github.io/agent-registry-protocol/spec/agent-registry-protocol-v0.9.0.html)
[![Validation](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/actions/workflows/validate.yml/badge.svg)](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/actions/workflows/validate.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/spec-CC%20BY%204.0-lightgrey.svg)](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/blob/main/LICENSE)
[![Code: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-lightgrey.svg)](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/blob/main/LICENSE-CODE)

**A modular authority-control protocol for governed agent identity, delegation, recognition, lifecycle, evidence, enforcement and redress.**

> An agent registry is not merely a directory. It is an authority control plane whose claims must be scoped, revocable, inspectable and enforceable.

## Repository status

| Attribute | Value |
|---|---|
| Portfolio tier | Flagship |
| Lifecycle | Active |
| Stability | v0.9.1 Implementation Accelerator over v0.9.0 Candidate Specification |
| Primary artifacts | Specification, schemas, API/event contracts, reference implementations, conformance and evidence |
| Release gate | `make release-check` |
| Candidate evidence | `artifacts/candidate-specification/evidence-bundle.json` |
| Authority | Community draft governed by `GOVERNANCE.md` |

## What v0.9.1 delivers

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

1. [Run the 15-minute implementation quickstart](docs/implementation-accelerator/01-15-minute-quickstart.md)
2. [Implementation Accelerator](docs/implementation-accelerator/index.md)
3. [Documentation home](docs/index.md)
4. [Authoritative v0.9.0 Candidate Specification](https://sankarshanmukhopadhyay.github.io/agent-registry-protocol/spec/agent-registry-protocol-v0.9.0.html)
5. [Candidate implementation guide](docs/candidate-specification-guide.md)
6. [ARPA–TRQP interoperability architecture](docs/architecture/trqp-arpa-interoperability.md)
7. [Migration from v0.5.0](docs/migration-v0.5.0-to-v0.9.0.md)
8. [Known limitations](KNOWN_LIMITATIONS.md)

## Validate and produce evidence

```bash
make setup
make release-check
```

The gate validates the complete schema and conformance surface, repository controls, service tests, v0.5.0 interoperability behavior, v0.9.0 candidate requirements, ARPA–TRQP mapping and vectors, independent adapter equivalence, loopback network discovery, durable event semantics and implementation reports.

## ARPA and TRQP

ARPA owns the authority, lifecycle, evidence, revocation, enforcement and federation control plane. TRQP is treated as an external, minimal read-only query interface. The optional v0.9.0 projection demonstrates how selected ARPA authorization and recognition state can be exposed without merging the protocols or implying cross-protocol conformance.

## Assurance boundary

The supplied implementations and loopback network tests are repository-controlled candidate evidence, not external certification or proof of universal interoperability. The release does not claim legal authority, production key custody, formal cryptographic review, independent TRQP approval, or completed revocation without enforcement acknowledgement. See [known limitations](KNOWN_LIMITATIONS.md), [AI usage](AI_USAGE.md), [governance](GOVERNANCE.md), and [security](SECURITY.md).
