---
layout: default
title: "ARPA A2A v1.0 Interoperability Profile"
nav_order: 82
parent: Protocol profiles
---

# ARPA A2A v1.0 Interoperability Profile

**Profile identifier:** `https://arpa.example/profiles/a2a/1.0`  
**ARPA implementation release:** v0.9.2  
**A2A protocol family:** 1.0  
**Status:** Versioned interoperability profile over the ARPA v0.9.0 Candidate Specification

## 1. Purpose and scope

This profile defines how A2A v1.0 Agent Cards, interfaces, skills, security declarations, extensions, tasks and artifacts are bound to ARPA records and evidence. It does not make A2A normative for ARPA-Core and does not reproduce A2A transport or task semantics.

ARPA provides canonical identity resolution, authority, delegation, lifecycle status, assurance, governance, revocation and evidence. A2A provides discovery metadata and interaction mechanics. An implementation claiming this profile MUST preserve that separation.

## 2. Mandatory non-implication rules

An A2A Agent Card, successful card signature check, declared skill, endpoint authentication, accepted task or completed task MUST NOT by itself imply:

- verified capability or fitness for purpose;
- delegated or transaction authority;
- principal consent;
- issuer competence;
- assurance level;
- governance recognition;
- legal permission; or
- continuing operational status.

A2A authentication answers whether a caller satisfied an endpoint access mechanism. ARPA authority evaluation answers whether the requested action is authorised in context.

## 3. Supported description profile

A conforming implementation MUST identify imported cards using `description_profile: a2a-agent-card-1.0`. It MUST record the exact retrieved representation in an Agent Description Reference and MUST validate its declared digest before relying on imported values.

A card signature MAY provide additional integrity and signer evidence. Signature verification MUST be recorded separately from ARPA recognition, competence, assurance and authority.

## 4. Public and extended cards

Implementations MUST classify each referenced representation as one of:

- `public`;
- `authenticated-extended`;
- `tenant-specific`; or
- `private`.

An authenticated or contextual card MUST NOT be promoted to a universal public description. Where disclosure depends on an audience or access context, the implementation MUST bind the reference to an `access_context_digest` and apply purpose limitation and retention controls.

## 5. Field and record mapping

The normative machine-readable mapping is `mappings/a2a-v1.0-arpa-mapping.yaml`.

| A2A concept | ARPA record or control | Required treatment |
|---|---|---|
| Agent Card identity and provider metadata | Agent Core / Description Reference | Import as self-declared unless independently supported |
| Agent interfaces | Service Endpoint and Deployment | Preserve each interface, protocol binding and protocol version separately |
| Skills | Capability Declaration | Import as `self_declared`; never infer verification or authority |
| Security schemes and requirements | Service Endpoint access requirements | Do not map to Authority Envelope |
| Card signature | Key Binding and evidence reference | Proves integrity relative to the signer only |
| A2A extension | Extension registry entry and relying-party policy | Fail closed for unsupported required extensions affecting authority or evidence |
| Task and context identifiers | Execution Receipt | Bind execution evidence to the A2A interaction |
| Artifacts | Execution Receipt artifact evidence | Use cryptographic digests, not artifact names, as evidence anchors |

## 6. Processing algorithm

Before initiating a consequential A2A task, a conforming relying implementation MUST:

1. resolve the canonical ARPA agent identifier;
2. validate agent, deployment, key and recognition status within policy freshness limits;
3. retrieve and integrity-check the applicable Agent Card representation;
4. select an advertised interface and supported A2A protocol version;
5. satisfy the interface authentication mechanism;
6. evaluate the relevant ARPA Authority Envelope and delegation chain;
7. issue or retain an authority Decision Receipt;
8. initiate the A2A task only after an affirmative decision;
9. correlate task, context, interface and protocol version in an Execution Receipt; and
10. retain artifact digests and terminal-state evidence.

Any indeterminate authority decision MUST fail closed for consequential actions.

## 7. Conflicts and precedence

Authoritative ARPA lifecycle, key, deployment, delegation, recognition and revocation state takes precedence over cached or freshly retrieved Agent Card statements. A conflict MUST be surfaced and recorded. Implementations MUST NOT silently elevate card content above registry state.

An unexpired cached card does not override a revoked key, suspended agent, quarantined deployment, expired delegation or withdrawn recognition.

## 8. Cancellation and revocation

A2A task cancellation is an interaction-level mechanism, not an authority revocation event. On relevant ARPA suspension or revocation, an enforcement implementation SHOULD deny new tasks and attempt to cancel affected active tasks. It MUST record cancellation attempts, acknowledgements, failures and any artifacts produced after the authoritative event.

## 9. Required extensions

An unsupported A2A extension marked required MUST cause rejection when it can affect identity, authority, evidence, task state, artifact interpretation or safe failure. The implementation MUST emit `ARPA-A2A-REQUIRED-EXTENSION-UNSUPPORTED`.

## 10. Evidence requirements

A conformance evidence bundle MUST include, as applicable:

- retrieved-card digest and retrieval time;
- signature verification outcome and verification method;
- selected interface, binding and protocol version;
- ARPA status and authority decision references;
- A2A task and context identifiers;
- terminal task state;
- artifact digests;
- extension support decisions; and
- revocation or cancellation enforcement evidence.

## 11. Conformance

Claiming this profile requires all vectors under `conformance/test-vectors/a2a-v1.0/` to pass and requires execution of `scripts/validate_a2a_interoperability.py`. Passing repository vectors demonstrates conformity of the supplied implementation artifacts only. It is not certification, legal recognition or proof of production deployment assurance.
