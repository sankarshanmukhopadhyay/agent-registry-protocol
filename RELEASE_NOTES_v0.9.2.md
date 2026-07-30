---
layout: default
title: "Release Notes v0.9.2"
nav_exclude: true
---

# Agent Registry Protocol v0.9.2

ARPA v0.9.2 adds a versioned, machine-verifiable interoperability profile for A2A v1.0 while preserving the v0.9.0 Candidate Specification as the normative protocol baseline.

## Highlights

- Adds the **ARPA A2A v1.0 Interoperability Profile**.
- Defines a machine-readable A2A-to-ARPA field and claim mapping.
- Preserves the separation between endpoint authentication and delegated authority.
- Models public, authenticated-extended, tenant-specific and private Agent Card representations.
- Extends Agent Description Reference and Agent Card extension schemas.
- Correlates A2A tasks, contexts, protocol versions, terminal states and artifact digests with ARPA Execution Receipts.
- Adds controlled A2A interoperability error codes.
- Adds six executable positive and negative conformance vectors.
- Integrates A2A validation into `make release-check`.

## Governance boundary

A2A Agent Cards remain discovery and routing inputs. A declared skill, successful endpoint authentication, valid card signature, accepted task or completed task does not by itself establish capability verification, delegated authority, principal consent, assurance, governance recognition or legal permission.

Authoritative ARPA lifecycle, key, deployment, delegation, recognition and revocation state takes precedence over Agent Card content and cache freshness.

## Compatibility

- **Normative ARPA specification:** v0.9.0 Candidate Specification
- **Implementation release:** v0.9.2
- **A2A interoperability profile:** A2A protocol family 1.0
- Existing ARPA-Core records remain compatible.
- A2A support is an optional profile and is not required for ARPA-Core conformance.

## Documentation architecture

A post-release documentation commit adds a single Start Here decision page, explicit normative and informative status boundaries, linked conformance artefacts, A2A-aware repository positioning, scenario-to-module mappings and machine-verifiable navigation assurance. No protocol, schema, API or normative conformance requirement changes.

A follow-up build fix makes the publication manifest permalink-aware, aligning clean Jekyll URLs such as `/docs/start-here/` with `_site/docs/start-here/index.html` during Pages validation.

## Validation

The release gate now includes:

```bash
python3 scripts/validate_a2a_interoperability.py
make release-check
```

Passing the supplied vectors demonstrates conformance of the repository implementation artifacts only. It does not constitute certification, legal recognition, production security assurance or independent interoperability validation.
