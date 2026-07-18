---
layout: default
title: "Production hardening"
parent: "Implementation Accelerator"
nav_order: 9
---
# Production hardening

The supplied service is a reference implementation, not a production product. Before production use, replace or harden the following boundaries:

| Boundary | Minimum control | Evidence |
|---|---|---|
| Key custody | HSM/KMS-backed keys, rotation and revocation | Key inventory and rotation logs |
| Authentication | Strong workload and administrator authentication | Access-control test report |
| Authorization | Policy engine with deny-by-default semantics | Positive and negative decision vectors |
| Storage | Encrypted, backed up, migration-controlled database | Restore test and schema migration records |
| Events | Durable, ordered, replay-safe transport | Replay and acknowledgement report |
| Monitoring | Health, latency, denial, stale-state and conflict alerts | Alert tests and dashboard snapshots |
| Redress | Named escalation, appeal and correction workflow | Completed exercise record |
| Availability | Defined SLO, recovery objectives and failover | Recovery exercise evidence |

No production claim should be made solely because the Docker Compose environment runs successfully.
