---
layout: default
title: "Federated pilot topology"
nav_exclude: true
---
# Federated pilot topology

Operate two registries under separate accountable authorities. Exchange only registry metadata, scoped recognition, canonical resolution results and replay-safe lifecycle events. Do not replicate private operational records unless the pilot governance agreement explicitly authorizes it.

```mermaid
flowchart LR
  RA[Registry A] <-- metadata and recognition --> RB[Registry B]
  RA --> EA[Evidence store A]
  RB --> EB[Evidence store B]
  GOV[Joint pilot governance] --> RA
  GOV --> RB
```
