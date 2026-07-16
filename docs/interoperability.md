# v0.5.0 Interoperability Guide

## Objective

The v0.5.0 release turns interoperability from a roadmap statement into a repeatable repository capability. Two independently configured registry fixtures exchange registry metadata, resolve a canonical agent record, verify recognition scope, propagate a revocation event, and record acknowledgement by a heterogeneous enforcement point.

## What is tested

| Gate | Expected evidence |
|---|---|
| Metadata discovery | Registry B parses Registry A metadata and confirms supported modules and profile claims |
| Canonical resolution | Registry B resolves the same canonical identifier and digest supplied by Registry A |
| Recognition | Registry B accepts only record types covered by an explicit recognition statement |
| Event continuity | Imported events have a contiguous sequence and stable event identifiers |
| Revocation propagation | A revocation emitted by Registry A reaches Registry B |
| Enforcement acknowledgement | A relying enforcement point records the revocation and stops authorising the affected subject |
| Policy portability | Equivalent JSON-rule and Python-reference evaluators return the same decision |
| Evidence integrity | The final evidence bundle carries deterministic SHA-256 digests for all imported artifacts |

## Run

```bash
make interop
```

The command writes:

```text
artifacts/interoperability/evidence-bundle.json
artifacts/interoperability/interoperability-report.json
```

A successful report has `passed: true` and contains the checks, fixture identities, imported record digests, revocation acknowledgement, policy-equivalence result, and limitations.

## Trust and authority boundaries

The demonstration verifies protocol behavior across two separately configured fixtures. It does not claim organisational independence, production federation, legal recognition, secure key custody, or external implementation conformance. Registry recognition remains explicit, scoped, time-bound, and revocable. Imported records do not become authoritative merely because they are technically retrievable.

## Extending the harness

An external implementation can replace either fixture by exporting the same exchange package documented in `interop/README.md`. Its report should identify implementation provenance, version, supported modules, profile claims, failed checks, and known limitations. An AI-generated or configuration-only variant does not count as an independent implementation.
