---
layout: default
title: "Your first registry"
parent: "Implementation Accelerator"
nav_order: 2
---
# Your first registry

A registry deployment begins with an explicit operating identity and declared capability boundary. The reference service exposes this through `GET /registry`.

The response declares the registry identifier, supported modules and profiles, authoritative base URI, status freshness expectation, event retention and conformance declaration location. Implementors should treat this document as a machine-readable promise whose accuracy is continuously testable.

## Copy this

Use `implementation-accelerator/config/registry.env.example` as the configuration baseline and `pilot-kit/checklists/registry-bootstrap.md` as the operator evidence checklist.

## Evidence produced

- reachable metadata endpoint;
- stable registry identifier;
- explicit protocol version;
- declared module and profile support;
- documented authoritative URI;
- event and status service expectations.
