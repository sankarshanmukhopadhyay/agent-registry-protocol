---
layout: default
title: Reference Implementation Architecture
parent: Documentation
nav_exclude: true
---

# Reference Implementation Architecture

The reference implementation contains a stateful registry, append-only event store, query resolver, materialized current-state projection and authority PDP. SQLite is used only for local reproducibility.

```mermaid
flowchart LR
  C[Client] --> API[REST API]
  API --> R[Authoritative Registry]
  R --> E[Append-only Events]
  E --> I[Projection / Index]
  API --> I
  API --> PDP[Authority Evaluator]
  PDP --> DR[Decision Receipt]
```

The service demonstrates protocol semantics. It does not provide production consensus, key custody, identity proofing, legal authorization or regulatory certification.
