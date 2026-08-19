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
| Events | Durable, scoped-ordering, replay-safe transport with poison-event isolation and acknowledgement after durable handoff | Operational resilience event report |
| Monitoring | Health, latency, denial, stale-state and conflict alerts | Alert tests and dashboard snapshots |
| Redress | Named escalation, appeal and correction workflow | Completed exercise record |
| Availability | Defined SLO, recovery objectives, bounded failover, load shedding/admission control and stabilized recovery | Partial-outage and recovery exercise evidence |

No production claim should be made solely because the Docker Compose environment runs successfully.

## Operational resilience assurance

Production deployments should treat retry, failover, event delivery, dependency protection, and sustained-load progress as one cross-cutting assurance surface. The normative safety properties are defined in [Specification §36.9](../../spec/agent-registry-protocol-v0.9.0.md#369-operational-resilience-assurance); the machine-readable declaration is `schemas/operational-resilience-declaration.schema.json`.

Minimum deployment evidence should include a failure-domain map, retry ownership and aggregate budgets, recovery stabilization criteria, event quarantine and durable-acknowledgement boundaries, dependency-amplification controls, and proof that safety-critical control-plane work continues to progress during query saturation. Fixed algorithms and timer values are deployment choices unless a governing profile or relying-party policy constrains them further.
