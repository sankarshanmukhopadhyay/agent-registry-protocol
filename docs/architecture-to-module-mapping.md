# Architecture-to-Module Mapping

| Architecture concern | Module | Primary artifacts |
|---|---|---|
| Agent identity and aliases | Core | Agent Core, Identifier Alias |
| Description integrity | Core | Agent Description Reference |
| Keys and endpoints | Core | Key Binding, Service Endpoint |
| Lifecycle and history | Core | Status, Event |
| Operator/controller/accountability graph | Relations | Relationship |
| Capability claims | Assurance | Capability Declaration, Capability Verification |
| Independent evaluation | Assurance | Assurance Claim |
| Delegation and scope | Authority | Authority Envelope |
| Decision explanation | Authority | Decision Receipt |
| Execution reconstruction | Evidence | Execution Receipt, Evidence references |
| Contestability | Evidence/Relations | Redress Record, Governance Record |
| Cross-registry reliance | Federation | Recognition Record |

Normative requirement identifiers in future revisions SHOULD use the form `ARPA-<MODULE>-<NUMBER>` so implementation reports can provide direct traceability.
