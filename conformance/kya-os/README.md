# KYA-OS → ARPA conformance profile

This directory contains the executable evidence for ARPA issue #12.

The profile is **informative**. It pressure-tests ARPA's ability to consume external runtime delegation/action evidence while preserving ARPA authority resolution.

## Required outcomes

Each vector records:

- external proof verification status;
- asserted subject/principal/delegation/action facts;
- ARPA governance facts needed for the decision;
- expected ARPA outcome;
- the proposition being exercised;
- the falsification condition.

The corpus must demonstrate both acceptance and fail-closed rejection. A vector is invalid if it collapses `proof_verified` into `authorized`.
