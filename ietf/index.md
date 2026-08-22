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

The checked-in Markdown file is the repository authoring source. RFCXML v3, plaintext, and HTML are deterministic build products generated and validated by GitHub Actions from that source.

- [Internet-Draft authoring source](draft-sankarshan-agent-registry-protocol.html)
- [Rendered Internet-Draft — HTML](generated/draft-sankarshan-agent-registry-protocol-00.html)
- [Rendered Internet-Draft — plaintext](generated/draft-sankarshan-agent-registry-protocol-00.txt)
- [RFCXML v3](generated/draft-sankarshan-agent-registry-protocol-00.xml)
- [Generated-artifact SHA-256 checksums](generated/SHA256SUMS)
- [Protocol extraction and provenance map](PROTOCOL_EXTRACTION.html)
- [Submission-readiness checklist](SUBMISSION_CHECKLIST.html)
- [Repository authoring guide](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/blob/main/ietf/README.md)

The Internet-Draft revision series is independent of ARPA semantic versions. The initial submission candidate is revision `-00`; later IETF revisions increment independently from ARPA project releases.

## Build, publication, and validation

Every GitHub Pages deployment installs the IETF authoring toolchain, runs `make ietf-check`, and publishes the resulting RFCXML v3, plaintext, and HTML artifacts under `/ietf/generated/`. The deployment fails if the IETF build or the complete publication validation fails.

The same generated outputs remain excluded from Git so they cannot drift independently from the checked-in authoring source. SHA-256 checksums are published with the rendered artifacts and retained in the Pages assurance artifact for build evidence.

Generated submission artifacts are intentionally not treated as independent project authority until the corresponding draft revision is reviewed and submitted.
