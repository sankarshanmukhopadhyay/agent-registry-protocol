# ARPA TypeScript implementation

This directory contains an **independent TypeScript interpretation** of the ARPA protocol, released as the TypeScript v0.3.0 track within ARPA v0.9.5. It improves implementation portability and cross-runtime assurance without sharing behavioural code with the Python reference evaluator.

## Use

```bash
npm install
npm run release-check
```

Start the development HTTP service:

```bash
npm run network-server
```

The exported local package surface includes `ArpaClient`, the thin server, authority/resolution functions, historical-resolution helpers, decision receipts, event continuity, A2A adapters and the in-memory development store.

## Protocol sources

The implementation consumes repository-owned normative/machine-verifiable sources directly:

- `../schemas/` — JSON Schema contracts;
- `../registries/` — governed code registries;
- `../conformance/test-vectors/` — observable protocol outcomes;
- `../spec/agent-registry-protocol-v0.9.0.md` — normative protocol requirements.

Behavioral code MUST NOT import or mechanically translate `../reference/` or `../scripts/reference_evaluator.py`.

## Evidence

Reports under `../artifacts/typescript/` cover deterministic vectors, historical resolution, A2A adapters, same-corpus cross-runtime equivalence and HTTP network interoperability.

## Assurance boundary

Discovery and A2A publication never imply authority. The server is development-grade and uses in-memory persistence. Repository ownership of both runtimes does not constitute the externally independent implementation evidence required for v1.0.
