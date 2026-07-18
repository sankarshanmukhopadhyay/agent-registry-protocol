---
layout: default
title: "Pilot readiness"
parent: "Implementation Accelerator"
nav_order: 8
---
# Pilot readiness

A pilot is ready only when technical execution, authority ownership and evidence retention are all explicit.

Run:

```bash
make pilot-check
```

The validator checks service health, metadata, agent resolution, status, allow and deny authority paths, events and fixture integrity. It writes a machine-readable report under `artifacts/pilot/`.

The automated report is necessary but not sufficient. Operators must also complete:

- `pilot-kit/checklists/governance-readiness.md`
- `pilot-kit/checklists/security-readiness.md`
- `pilot-kit/checklists/operations-readiness.md`
- `pilot-kit/checklists/exit-and-revocation.md`

The pilot authority must sign off the human-governed controls that cannot be inferred from service responses.
