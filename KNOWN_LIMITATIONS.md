# Known Limitations

The v0.4.0 reference implementation is an interoperability demonstrator, not a production registry.

- Proof fields are schema-modeled, but the service does not manage production signing keys or verify every proof suite.
- The authority evaluator implements the deterministic policy subset exercised by the conformance vectors; it is not a universal policy engine.
- SQLite provides reproducible local state, not distributed consensus or high availability.
- Federation records and recognition schemas are present, but no production peer-to-peer federation service is provided.
- Identity proofing, legal capacity, liability, accreditation and regulatory recognition remain ecosystem responsibilities.
- Event delivery is exposed through replayable polling; production webhook authentication and durable message-broker bindings require deployment-specific work.
- Agent Card interoperability is a generic mapping and does not endorse any vendor implementation.
- Independent interoperability testing remains necessary before Candidate Specification status.
