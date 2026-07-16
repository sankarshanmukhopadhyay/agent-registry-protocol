# ARPA Core Identity and Discovery Profile

**Status:** Normative profile for ARPA v0.5.0  
**Module:** ARPA-Core  
**Conformance profile:** Profile A

## 1. Purpose

This profile defines the minimum interoperable registry. It establishes resolvable identity and metadata integrity without claiming delegated authority, assurance, accountability, safety or universal trust.

## 2. Required record support

A conforming implementation MUST support Agent Core, Key Binding, Service Endpoint, Status, Event, Agent Description Reference, Identifier Alias and Conformance Declaration records.

## 3. Required operations

- resolve a canonical agent identifier;
- resolve an active or historical alias;
- retrieve current and point-in-time lifecycle status;
- retrieve metadata references and verify their digests;
- retrieve key bindings and endpoints;
- enumerate lifecycle and metadata events;
- search by explicitly supported fields;
- publish registry metadata and a conformance declaration.

Unsupported Authority, Assurance, Evidence or Federation operations MUST return `ARPA-OP-NOT-SUPPORTED`.

## 4. Identifier requirements

Identifiers MUST be persistent and non-reassignable. Terminal identifiers MUST remain resolvable as terminal records. An implementation MUST distinguish never-issued, access-controlled and terminal records.

## 5. Integrity commitment

An Agent Description Reference MUST identify the representation, canonicalization method, digest algorithm, digest value and retrieval location. A successful digest check establishes content integrity only. It does not establish that the description is true or independently verified.

## 6. Freshness

Every current-state response MUST disclose authoritative source, `observed_at`, `issued_at`, `valid_until` or maximum age, and projection lag where applicable.

## 7. Events

Events MUST be ordered per source, replayable within the published retention window, deduplicable by event identifier and attributable to an issuer. Consumers MUST be able to detect sequence gaps.

## 8. Security

Authoritative records MUST be tamper-evident. Implementations MUST verify issuer competence for registry administration, alias issuance, status transitions and key binding. Unknown critical extensions MUST fail closed.

## 9. Conformance evidence

Profile A conformance requires schema validation, protocol contract tests, identifier resolution vectors, digest vectors, lifecycle vectors, event replay vectors and a machine-readable implementation report.
