# Implementor Guide

## Build order

1. Implement ARPA-Core schemas and identifier resolution.
2. Add append-only events and point-in-time reconstruction.
3. Publish the OpenAPI contract and conformance declaration.
4. Add typed relationships and issuer-competence policy.
5. Add assurance or authority only when the relying use case requires them.
6. Integrate enforcement and revocation acknowledgement before claiming Profile C or D.

## Authority boundaries

The registry operator may administer records but is not automatically competent to issue every relationship, delegation or assurance claim. Implement issuer-competence policy as a separate decision table and preserve evidence for each acceptance decision.

## Evidence

Every conformance run should emit a dated machine-readable report containing implementation version, supported modules, test-vector results, limitations and artifact digests.
