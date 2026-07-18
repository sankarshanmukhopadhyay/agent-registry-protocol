---
layout: default
title: "Release Policy"
nav_exclude: true
---

# Release Policy

ARPA uses semantic versioning for repository releases and maintains a separate schema-version track where documented in `schemas/README.md`.

A release is warranted for a new normative capability, machine-verifiable artifact, material interoperability change, completed conformance gate, security or correctness fix, or adoption-ready workflow. Editorial-only changes should normally be batched.

## Readiness gates

A release candidate MUST pass `make validate`, `make test`, `make interop`, and `make report`. Release notes MUST state operational impact, compatibility, evidence produced, security implications, limitations, and migration requirements.

A Candidate Specification requires at least two independently developed interoperable implementations. Repository fixtures, generated variants, and AI-produced derivatives do not satisfy that gate.
