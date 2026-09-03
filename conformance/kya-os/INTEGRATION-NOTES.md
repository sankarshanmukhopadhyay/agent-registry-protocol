# Integration limits

- The profile consumes a boolean external proof-verification result; it does not implement KYA-OS proof verification.
- MCP is represented only as an optional host-protocol binding string and has no normative ARPA semantics here.
- DIDs, VCs, KYA-specific identifiers, and KYA-specific cryptographic algorithms are not required by the ARPA core.
- Unsupported delegation semantics fail as `projection-rejected`; they are not normalized heuristically.
- ARPA recognition, competence, lifecycle, conflict, scope and historical evaluation remain independent inputs to the governed decision.
