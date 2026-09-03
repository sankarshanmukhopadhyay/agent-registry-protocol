# KYA-OS → ARPA governed delegation and action-evidence profile

Status: **informative investigation profile**

Tracking issue: #12

This profile tests whether externally verified KYA-OS runtime evidence can be consumed by ARPA without turning cryptographic validity, discovery metadata, or a host-protocol binding into governance authority.

The integration boundary is deliberately one-way:

```text
KYA-OS / host-protocol binding
        |
        | verified external evidence
        v
KYA-OS → ARPA evidence adapter
        |
        v
ARPA authority resolution
        |
        v
governed decision + reproducible evidence
```

## Non-implications

1. A valid KYA-OS proof does **not** imply ARPA authorization.
2. A signed discovery/publication record does **not** imply ARPA recognition or authority.
3. Possession of a signing key or credential does **not** prove competence to delegate.
4. MCP, DIDs, VCs, or a KYA-specific proof mechanism do **not** become mandatory ARPA primitives.
5. The adapter must reject semantic loss rather than silently widen or narrow authority.

## Evidence separation

The adapter output records external evidence assertions separately from the ARPA decision record. ARPA remains responsible for recognition, delegator competence, scope intersection, lifecycle, conflict/federation handling, evaluation time, enforcement state, and final governed outcome.

## Investigation outcome

The current implementation should be accepted only if the executable corpus demonstrates that valid external evidence can be projected without privilege amplification and that ARPA can independently deny otherwise valid evidence when governance state requires it.
