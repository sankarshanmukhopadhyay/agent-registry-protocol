---
layout: default
title: "Start Here"
nav_exclude: false
nav_order: 2
document_status: informative
permalink: /docs/start-here/
---

# Start here

ARPA has several entry points because evaluation, pilot deployment, conformance review and protocol integration produce different evidence. Choose the journey that matches the decision you need to make.

| Objective | Entry point | Primary commands or artefacts | Evidence produced | Status |
|---|---|---|---|---|
| Understand the protocol architecture | [Protocol modules](protocol-modules.md) | Module and dependency model | Explicit scope and non-implication rules | Informative |
| Validate and run the reference service locally | [Quickstart](quickstart.md) | `make setup`, `make validate`, `make test`, `make run` | Schema, vector, test and service results | Informative |
| Stand up a pilot registry | [15-minute quickstart](implementation-accelerator/01-15-minute-quickstart.md) | `make pilot-up`, `make pilot-seed`, `make pilot-check` | Pilot-readiness report and decision evidence | Informative |
| Prepare a repository release | [Candidate Specification implementation guide](candidate-specification-guide.md) | `make setup`, `make release-check` | Complete repository release-gate evidence | Informative process |
| Claim implementation conformance | [Conformance Guide](conformance-guide.md) | Declaration, report and profile evidence | Reviewable conformance package | Profile-dependent |
| Integrate A2A Agent Cards and tasks | [ARPA A2A v1.0 Interoperability Profile](../spec/profiles/arpa-a2a-v1.0-interoperability-profile.md) | Mapping, schemas and test vectors | A2A interoperability evidence | Optional profile normative |

## Status and version boundary

- **Normative:** the [ARPA Candidate Specification v0.9.0](../spec/agent-registry-protocol-v0.9.0.md) defines the core protocol requirements.
- **Profile normative:** optional profiles define additional requirements only when an implementation claims that profile.
- **Informative:** guides, scenarios and accelerator assets explain implementation and deployment without changing normative requirements.

ARPA v0.9.2 is the current implementation and interoperability release. It preserves the v0.9.0 Candidate Specification as the normative baseline and adds implementation artefacts and optional profiles, including A2A v1.0 interoperability.

## Complete catalogue

Use the [documentation catalogue](index.md) when you need the full specification, governance, implementation, conformance, interoperability and scenario surface.


## v0.9.3 A2A registry convergence

See the [A2A Registry Integration Guide](a2a-registry-integration-guide.md) for publication, caller-visible discovery, resolve/snapshot, compatibility and authority-boundary semantics.
