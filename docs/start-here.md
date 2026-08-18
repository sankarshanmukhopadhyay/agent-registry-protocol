---
layout: default
title: "Start Here"
nav_exclude: false
nav_order: 2
document_status: informative
permalink: /docs/start-here/
---

# Start here

ARPA is easier to navigate when you begin with the **decision you need to make**, not with the repository directory structure.

## Choose your journey

| You need to… | Go to | Primary outcome |
|---|---|---|
| Understand ARPA's trust and authority model | [1. Understand ARPA](understand.md) | Correct conceptual boundaries and module selection |
| Implement or evaluate code | [2. Build ARPA](build.md) | Working protocol implementation |
| Test a conformance or release claim | [3. Assure & Conform](assure.md) | Machine-verifiable assurance evidence |
| Deploy or govern a registry | [4. Operate ARPA](operate.md) | Operational controls and readiness evidence |
| Connect A2A, TRQP or another system | [5. Integrate & Interoperate](integrate.md) | Explicit protocol-boundary mapping |
| Contribute, release or review governance | [6. Govern & Contribute](govern.md) | Reviewable change-control and repository evidence |

## Version boundary

- **Normative baseline:** [ARPA Candidate Specification v0.9.0](../spec/agent-registry-protocol-v0.9.0.md).
- **Current implementation release:** v0.9.5.
- **Normative protocol baseline:** v0.9.0 Candidate Specification; the TypeScript implementation consumes the v0.9.4 historical-resolution and conformance artifacts as part of the v0.9.5 assurance surface.

Guides and implementation code do not silently redefine normative requirements. Optional profiles become normative only when that profile is claimed.

## Developer shortcut

If you are here to build something, start with [Build ARPA](build.md), then run `make release-check-all` and review the evidence described in [Assure & Conform](assure.md).

For every rendered document and historical release note, use the [Documentation catalogue](index.md).

## Standards engagement

ARPA maintains a separate IETF Internet-Draft authoring track for the interoperable protocol core. The initial individual-draft candidate is `draft-sankarshan-agent-registry-protocol-00`. It is not yet an IETF work item and does not replace the ARPA Candidate Specification.

- [IETF authoring track](../ietf/)
- [Protocol extraction map](../ietf/PROTOCOL_EXTRACTION.md)
- [`-00` submission checklist](../ietf/SUBMISSION_CHECKLIST.md)

Use this path when reviewing ARPA for IETF submission, protocol-scope reduction, IANA requirements, or overlap with existing IETF work.
