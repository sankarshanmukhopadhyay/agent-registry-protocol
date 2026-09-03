# Expected corpus outcomes

| Vector | Property | Expected |
|---|---|---|
| KYA-ARPA-01 | valid proof + valid governed authority | allow |
| KYA-ARPA-02 | valid proof + incompetent delegator | deny |
| KYA-ARPA-03 | valid proof + suspended agent | deny |
| KYA-ARPA-04 | revoked + enforcement convergence incomplete | deny + convergence finding |
| KYA-ARPA-05 | unresolved competent-source conflict | indeterminate |
| KYA-ARPA-06 | current proof vs historical unauthorized time | deny |
| KYA-ARPA-07 | discovery evidence without recognized authority | deny |
| KYA-ARPA-08 | lossy semantic projection | reject |
| KYA-ARPA-09 | unverifiable/tampered evidence | reject before authority inference |
| KYA-ARPA-10 | narrowed sub-delegation | allow without privilege amplification |

The central regression property is that `proof_verified=true` is compatible with `deny`, `indeterminate`, or `reject` when ARPA governance state requires it.
