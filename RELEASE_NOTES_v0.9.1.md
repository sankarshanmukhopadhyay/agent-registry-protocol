---
layout: default
title: "Release Notes v0.9.1"
nav_exclude: true
---
# Agent Registry Protocol v0.9.1
## Implementation Accelerator & Pilot Readiness

v0.9.1 is an implementation adoption release. It preserves the v0.9.0 Candidate Specification as the normative protocol baseline while adding an executable path from repository clone to pilot-readiness evidence.

## Highlights

- 15-minute Docker Compose quickstart;
- canonical Acme sample registry and governed agent fixtures;
- progressive implementation journey covering registry, authority, agent, delegation and federation;
- API consumer assets for curl/HTTP, Postman and Insomnia;
- automated pilot-readiness validator and evidence report;
- governance, security, operations and exit checklists;
- deployment profiles and production-hardening boundaries;
- first-class GitHub Pages Implementation Accelerator navigation.

## Compatibility

No normative v0.9.0 requirement is removed or weakened. The reference service advertises protocol version `0.9.0` and implementation release `0.9.1`; the normative specification remains `spec/agent-registry-protocol-v0.9.0.md` until the stable specification is advanced.

## Assurance boundary

Passing `make pilot-check` demonstrates repository-controlled reference behaviour. It is not certification, production authorization, external interoperability proof or approval of an operator's governance arrangements.
