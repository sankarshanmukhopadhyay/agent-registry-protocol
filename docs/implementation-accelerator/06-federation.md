---
layout: default
title: "Federation starter"
parent: "Implementation Accelerator"
nav_order: 6
---
# Federation starter

Federation is introduced only after local authority and lifecycle behaviour are proven. A pilot federation should contain two independently operated registries, explicit recognition scope, bounded metadata exchange and replay-safe event handling.

The v0.9.1 payload supplies a federation topology template in `pilot-kit/topologies/federated-pilot.md`. It does not claim universal interoperability. The acceptance condition is evidence that both registries can discover declared metadata, preserve authoritative provenance and fail closed when recognition or freshness cannot be established.
