---
layout: default
title: "TGA Agentic Governance Alignment"
nav_exclude: true
permalink: /docs/architecture/tga-agentic-governance-alignment/
document_status: informative
---

# Trust Graph Artifacts agentic-governance alignment

The Trust Graph Artifacts (TGA) **Agentic Systems Architecture and Governance** guide describes a protocol-neutral architecture for bounded jobs, legitimate authority, delegation, capability separation, governed execution, evidence, revocation, remediation, and assurance.

ARPA is a concrete realization of selected **discovery, authority-control, lifecycle, federation, and evidence** responsibilities in that architecture. This relationship is informative and optional: adopting the TGA guide does not require ARPA, and ARPA does not depend on TGA for protocol authority.

## Authority boundary

```text
TSMM  -> canonical trust-system semantics
TGA   -> generic agentic governance patterns and assurance guidance
TIS   -> portable executable contracts
ARPA  -> agent-registry and authority-control protocol realization
```

ARPA remains authoritative for its modules, normative requirements, controlled vocabulary, conformance profiles, API/event behavior, and implementation evidence. TGA remains authoritative for its guide, patterns, assurance cases, and guide-level negative-test methodology.

## Four-plane placement

| Plane | TGA architectural responsibility | ARPA contribution |
|---|---|---|
| Discovery | locate a persistent role/agent without treating discovery as permission | ARPA-Core registration, lifecycle, discovery and historical resolution |
| Authority control | determine whether a bounded effect is legitimate now | ARPA-Relations + ARPA-Authority |
| Execution | perform an admitted job through constrained capabilities and enforcement | outside ARPA's general responsibility; ARPA may supply authority/evidence inputs |
| Evidence and assurance | prove authority, decisions and consequential action are reconstructable | ARPA-Assurance + ARPA-Evidence |

ARPA-Federation contributes governed recognition and withdrawal across registry domains; technical federation alone does not create governance recognition.

## Shared architectural invariants

An ARPA implementation used within the TGA guide must preserve at least these rules:

1. identity does not imply authority;
2. registration or discovery does not imply permission to act;
3. capability does not imply permission;
4. a relationship does not imply delegated authority;
5. delegated scope may narrow but not silently expand;
6. revocation is incomplete until relevant enforcement surfaces converge;
7. technical federation does not imply governance recognition;
8. consequential action must remain reconstructable;
9. successful execution does not prove a legitimate effect.

## Module mapping

| Guide concern | ARPA module(s) |
|---|---|
| persistent agent identity and lifecycle | ARPA-Core |
| principal/operator relationships | ARPA-Relations |
| scoped capability assurance | ARPA-Assurance |
| delegation and authority evaluation | ARPA-Authority |
| receipts, reconstruction and audit | ARPA-Evidence |
| cross-domain recognition | ARPA-Federation |

## Responsibilities intentionally outside ARPA

The TGA guide also covers concerns that are not ARPA protocol responsibilities, including job decomposition, model/runtime orchestration, capability brokering, policy-enforcement implementation, fan-out convergence, generic effect-admission architecture, and TIS portable-contract selection.

This prevents the registry/control plane from being mistaken for the complete agentic runtime.

## Machine-readable declaration

The repository declaration is:

```text
interop/tga-agentic-governance-alignment.json
```

It is checked by `scripts/validate_tga_alignment.py` as part of `make validate` and therefore `make release-check-all`.

The reciprocal TGA declaration is maintained by TGA under `bindings/arpa/tga-arpa-agentic-governance-alignment.json`.

Neither declaration constitutes external certification or cross-repository conformance.
