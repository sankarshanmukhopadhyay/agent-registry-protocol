---
layout: default
title: "IETF Internet-Draft Track"
permalink: /ietf/
nav_exclude: true
---

# ARPA IETF Internet-Draft Track

This is the publication landing page for ARPA's **Agent Registry Protocol** Internet-Draft authoring track.

The current individual-draft candidate is:

`draft-sankarshan-agent-registry-protocol-00`

The draft is **not yet submitted** and does not imply IETF adoption, consensus, or working-group status.

## What is standardized here

The IETF track extracts the interoperable protocol core from the broader ARPA Candidate Specification:

- identifiers and registry resources;
- typed relationships;
- bounded delegated authority;
- lifecycle and status;
- registration, discovery, and current resolution;
- point-in-time historical resolution;
- event semantics;
- HTTP processing and error behavior;
- versioning and extensibility;
- security and privacy considerations; and
- prospective IANA actions.

Project governance, conformance programmes, A2A/TRQP profiles, deployment guidance, and assurance evidence remain supporting ARPA artifacts unless standardized separately.

## Authoring and assurance artifacts

- [Internet-Draft source](draft-sankarshan-agent-registry-protocol.html)
- [Protocol extraction and provenance map](PROTOCOL_EXTRACTION.html)
- [Submission-readiness checklist](SUBMISSION_CHECKLIST.html)
- [Repository authoring guide](README.html)

The Internet-Draft revision series is independent of ARPA semantic versions. The initial submission candidate is revision `-00`; later IETF revisions increment independently from ARPA project releases.

## Build and validation

The repository builds the Markdown source to RFCXML v3, plaintext, and HTML through the dedicated IETF workflow and Make targets. Repository validation also checks the IETF source before release gating.

Generated submission artifacts are intentionally not treated as project authority until the corresponding draft revision is reviewed and submitted.
