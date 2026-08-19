---
layout: default
title: "Operational resilience assurance"
nav_order: 8
---
# Operational resilience assurance

ARPA treats operational resilience as **executable governance across failure domains**. Profiles A-D describe increasing trust and consequence requirements; resilience is cross-cutting and therefore is not a fifth profile.

A deployment making a production or operational-conformance claim publishes an [Operational Resilience Declaration](../schemas/operational-resilience-declaration.schema.json) and evidence from the operational-resilience conformance suite.

## Assurance contract

| Control surface | Required claim | Evidence |
|---|---|---|
| Retry ownership | One declared retry owner and aggregate budget per failure domain | Lost-response and nested-retry vectors |
| Partial outage | Bounded fan-out, reduced-capacity control and stabilized recovery | Partial-outage and recovery-flapping vectors |
| Events | Explicit ordering scope, poison-event isolation and durable acknowledgement boundary | Head-of-line and acknowledgement-order vectors |
| Dependencies | Bounded concurrent-miss amplification and freshness-safe caching | Dependency amplification vector |
| Sustained load | Safety-critical control-plane work continues to make bounded progress | Revocation-under-load vector |

The assurance target is an observable property, not a mandated implementation technique. A service may use request coalescing, queues, admission control, service-mesh capabilities, replicated state, or other mechanisms provided the declared bounds and evidence are satisfied.

## Reference failure-domain map

```yaml
failure_domains:
  - id: registry-query
    components: [client, gateway, registry]
    retry_owner: client
    aggregate_retry_budget: 3
    maximum_retry_horizon_ms: 10000

  - id: authority-event-delivery
    components: [publisher, event-transport, enforcement-point]
    retry_owner: event-transport
    aggregate_retry_budget: 5
    maximum_retry_horizon_ms: 30000
    acknowledgement_boundary: durable-event-store
    ordering_scope: authority-envelope
```

The values above are illustrative rather than protocol-wide constants. Deployments must choose bounds appropriate to their architecture and consequence model and must expose those bounds in their declaration.

## Evidence boundary

Run:

```bash
python3 scripts/validate_operational_resilience.py
```

The generated `artifacts/operational-resilience/evidence-bundle.json` proves only that the repository-owned modeled fixtures produce the expected outcomes. Production claims require deployment-specific load, failure-injection, recovery, and observability evidence.

## RAHP disposition

This assurance surface was added in response to the review-required resilience gaps recorded in `sankarshanmukhopadhyay/rahp-toolkit#19`. ARPA adopts the safety outcomes while intentionally avoiding requirements for a specific retry library, cache implementation, queue product, service mesh, or fixed infrastructure timer.
