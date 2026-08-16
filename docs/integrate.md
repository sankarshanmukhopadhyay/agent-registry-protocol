---
layout: default
title: "5. Integrate & Interoperate"
nav_exclude: false
nav_order: 7
permalink: /docs/integrate/
document_status: informative
---

# Integrate and interoperate

ARPA is designed to compose with adjacent protocols without collapsing their trust semantics into ARPA or importing theirs as implicit authority.

## Integration paths

| Integration | Guide/profile | Boundary to preserve |
|---|---|---|
| A2A Agent Cards | [A2A Registry Integration Guide](a2a-registry-integration-guide.md) | Publication/discovery is not authority |
| A2A protocol profile | [ARPA A2A v1.0 Profile](../spec/profiles/arpa-a2a-v1.0-interoperability-profile.md) | Task completion is not ARPA authorization |
| TRQP | [ARPA–TRQP architecture](architecture/trqp-arpa-interoperability.md) | TRQP remains a read-only projection interface |
| General registry exchange | [Interoperability guide](interoperability.md) | Recognition and authority remain scoped |

## TypeScript integration surface

The v0.9.5 development track provides:

- a thin Node.js HTTP service;
- an `ArpaClient` for registry discovery, resolution and authority evaluation;
- A2A publication projection helpers;
- conservative Agent Card compatibility classification;
- Python↔TypeScript HTTP interoperability evidence.

See [TypeScript implementation](typescript-implementation.md) for supported and deferred behaviour.
