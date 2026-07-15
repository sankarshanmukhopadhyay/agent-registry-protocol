# ARPA Protocol Modules

ARPA is a composable protocol family. Conformance to a lower module does not imply support for, or a positive result from, a higher module.

| Module | Normative responsibility | Depends on |
|---|---|---|
| ARPA-Core | Persistent identity, metadata integrity, key binding, lifecycle, discovery, historical resolution | None |
| ARPA-Relations | Typed relationships and issuer competence | ARPA-Core |
| ARPA-Assurance | Capability declaration/verification and scoped assurance | ARPA-Core, ARPA-Relations |
| ARPA-Authority | Delegation, authority evaluation, conditions, prohibitions and decision receipts | ARPA-Core, ARPA-Relations |
| ARPA-Evidence | Execution receipts, reconstruction, evidence retention and audit | ARPA-Core; ARPA-Authority for delegated action |
| ARPA-Federation | Recognition, foreign-record resolution and withdrawal | ARPA-Core, ARPA-Relations |

## Non-implication rules

1. ARPA-Core registration MUST NOT imply authority, assurance, accountability, safety or suitability.
2. A relationship MUST NOT imply delegated authority unless represented by an Authority Envelope.
3. Capability declarations MUST be treated as self-declared unless linked to a competent Capability Verification or Assurance Claim.
4. Technical federation MUST NOT imply governance recognition.
5. Unsupported operations MUST return `ARPA-OP-NOT-SUPPORTED`; they MUST NOT be converted into affirmative results.

## Profile mapping

| Profile | Required modules |
|---|---|
| A: Discovery | ARPA-Core |
| B: Accountable Operations | ARPA-Core, ARPA-Relations, ARPA-Assurance, ARPA-Evidence |
| C: Delegated Authority | Profile B plus ARPA-Authority |
| D: High Assurance | Profile C plus ARPA-Federation and stronger operational/governance evidence |
