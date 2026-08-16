---
layout: default
title: "Known limitations"
nav_exclude: true
---

# Known limitations

ARPA v0.9.0 is a Candidate Specification, not a stable v1.0 release.

- The Python, independent projection and TypeScript implementation paths are separately structured but maintained in the same repository; external independently operated implementation evidence remains required for v1.0.
- The TypeScript v0.2.0 track covers shared deterministic conformance, historical-resolution reliance, decision receipts and event continuity, but it does not yet provide the stateful HTTP/client network surface, production persistence, proof verification, issuer-competence resolution or federation behavior of a complete deployment.
- Network federation is demonstrated over loopback endpoints, not a production multi-operator deployment.
- Durable event behavior is demonstrated with SQLite semantics, not a production message broker or multi-region system.
- Proof and key-management artifacts define integration boundaries and fixtures, not certified custody or formal cryptographic assurance.
- The ARPA–TRQP projection is informative and does not claim approval by, or conformance certification from, the TRQP project.
- TRQP response details may not preserve all ARPA delegation, condition, evidence, redress or enforcement information.
- Legal recognition, regulated-sector compliance, production availability and operational SLAs remain deployment responsibilities.
