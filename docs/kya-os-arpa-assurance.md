# Assuring a KYA-OS → ARPA integration

This walkthrough is informative and supports issue #12.

## Integrate

1. Verify KYA-OS evidence using the KYA-OS implementation or verifier responsible for that proof format.
2. Project only representable identity, delegation, temporal, action and provenance facts into the profile evidence contract.
3. Set `projection_lossless=false` when ARPA-required semantics cannot be preserved. Do not guess or widen scope.
4. Supply independent ARPA context for recognition, delegator competence, lifecycle, scope, evaluation time, source conflict and enforcement convergence.
5. Evaluate with `reference/kya_os_adapter.py` or an equivalent implementation preserving the same boundary.

## Assure

Run:

```bash
python3 scripts/validate_kya_os_profile.py
pytest -q tests/test_validate_kya_os_profile.py
```

The corpus deliberately includes verified proofs that ARPA denies, an unresolved conflict that remains indeterminate, a lossy projection that is rejected, and historical authority that differs from current proof validity.

Passing these checks demonstrates the profile's internal authority-boundary contract. It does **not** claim KYA-OS conformance, verify KYA cryptography, certify an implementation, or prove production interoperability with a live KYA-OS deployment.

## Integration choice

The evidence supports **an informative adapter/profile**, not a KYA-OS dependency in the ARPA core. A future generic external delegation/action-evidence interface remains possible if additional independent profiles demonstrate a stable protocol-neutral boundary.
