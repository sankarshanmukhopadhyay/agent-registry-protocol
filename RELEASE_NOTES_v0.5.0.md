---
layout: default
title: "ARPA v0.5.0: Interoperability and Evidence Release"
nav_exclude: true
---

# ARPA v0.5.0: Interoperability and Evidence Release

ARPA v0.5.0 advances the community draft from an implementation package to a reproducible interoperability release. It introduces a two-registry exchange harness, scoped recognition, revocation propagation and enforcement acknowledgement, portable policy evaluation, and a deterministic evidence bundle.

## Operational impact

Implementers can now run `make interop` to test metadata discovery, canonical resolution, recognition boundaries, event continuity, revocation handling, enforcement convergence, and policy-equivalent decisions. The resulting machine-readable report and evidence bundle can be retained, compared, and attached to implementation reviews.

## Added

- two separately configured registry fixtures and exchange package;
- interoperability runner with eight executable gates;
- revocation acknowledgement evidence for a heterogeneous enforcement point;
- portable JSON policy and two evaluation adapters;
- interoperability report and deterministic evidence bundle;
- flagship repository status, documentation landing page, release policy, GitHub Pages configuration, issue forms, pull-request controls, and validation workflow;
- `AI_USAGE.md` defining permitted assistance, human authority, disclosure, and prohibited assurance claims.

## Changed

- advanced specification, API, event, registry, reference-service, report, and citation metadata to v0.5.0;
- made release readiness executable through `make release-check`;
- clarified that repository fixtures do not satisfy the independent-implementation gate;
- aligned the README and roadmap with adoption, evidence, authority boundaries, and interoperability outcomes.

## Compatibility

The record schema track remains `1.0.0`. Existing v0.5.0 records remain valid. The release adds interoperability artifacts and implementation behavior without changing required record fields.

## Security and governance

Revocation is treated as incomplete until an enforcement point acknowledges the event and changes its resulting decision. Recognition remains explicit and scoped; technical exchange does not create governance recognition or transfer authority. The release does not add production key custody, network federation, consensus, or external certification.

## Validation

Release readiness requires successful schema and fixture validation, conformance vectors, extended governance vectors, reference-service tests, repository baseline checks, interoperability execution, and implementation-report generation.

## Known limitations

The two fixtures are maintained in one repository and are not independent implementations. Transport is file-based and deterministic. Cryptographic proof suites, production key management, durable broker delivery, and external policy engines remain future work.
