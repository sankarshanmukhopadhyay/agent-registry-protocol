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

The v0.9.1 adversarial-hardening rules that affect this protocol core are synchronized into the IETF authoring source set. They cover monotonic delegation intersection, temporal boundaries, non-applicability, authoritative conflict, revocation effectiveness versus enforcement convergence, decision reproducibility and proof-input semantics.

Project governance, conformance programmes, A2A/TRQP profiles, deployment guidance, and assurance evidence remain supporting ARPA artifacts unless standardized separately.

## Authoring and assurance artifacts

The checked-in IETF authoring source set consists of the base draft and the v0.9.1 protocol-hardening fragment. The build inserts the fragment before the draft back matter and then generates RFCXML v3, plaintext, and HTML deterministically.

- [Internet-Draft base authoring source](draft-sankarshan-agent-registry-protocol.html)
- [v0.9.1 protocol-hardening source fragment](fragments/adversarial-hardening.html)
- [Rendered Internet-Draft — HTML](generated/draft-sankarshan-agent-registry-protocol-00.html)
- [Rendered Internet-Draft — plaintext](generated/draft-sankarshan-agent-registry-protocol-00.txt)
- [RFCXML v3](generated/draft-sankarshan-agent-registry-protocol-00.xml)
- [Generated-artifact SHA-256 checksums](generated/SHA256SUMS.txt)
- [Protocol extraction and provenance map](PROTOCOL_EXTRACTION.html)
- [Submission-readiness checklist](SUBMISSION_CHECKLIST.html)
- [Repository authoring guide](https://github.com/sankarshanmukhopadhyay/agent-registry-protocol/blob/main/ietf/README.md)

The Internet-Draft revision series is independent of ARPA semantic versions. The initial submission candidate is revision `-00`; later IETF revisions increment independently from ARPA project releases.

## Build, publication, and validation

Every GitHub Pages deployment installs the IETF authoring toolchain, runs `make ietf-check`, and publishes the resulting RFCXML v3, plaintext and HTML artifacts under `/ietf/generated/`. The dedicated IETF workflow also runs whenever an IETF source or build input changes. The deployment fails if the IETF build or complete publication validation fails.

A project-level specification change does not automatically edit the Internet-Draft source. Protocol-core semantics must be explicitly synchronized into the IETF authoring source set. Once synchronized, generation is automatic: GitHub Actions rebuilds the RFCXML/TXT/HTML and Pages republishes the validated outputs.

Generated outputs remain excluded from Git so they cannot drift independently from checked-in authoring inputs. SHA-256 checksums are published with the rendered artifacts and retained in the Pages assurance artifact for build evidence.

Generated submission artifacts are intentionally not treated as independent project authority until the corresponding draft revision is reviewed and submitted.
