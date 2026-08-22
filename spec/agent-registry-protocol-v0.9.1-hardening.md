---
layout: default
title: "ARPA v0.9.1 Adversarial Hardening"
nav_exclude: true
---

# ARPA v0.9.1 Adversarial Hardening

**Status:** Candidate Specification amendment  
**Applies to:** ARPA v0.9.0 Candidate Specification  
**Version:** 0.9.1  
**Date:** 2026-08-22  
**License:** CC BY 4.0

## Status and authority

This document is a normative hardening amendment to the ARPA v0.9.0 Candidate Specification. It does not replace the architecture or record model in `agent-registry-protocol-v0.9.0.md`; it closes ambiguities that can otherwise permit divergent or adversarially permissive implementations. For ARPA v0.9.1 conformance, the v0.9.0 Candidate Specification and this amendment MUST be evaluated together. Where this amendment narrows or clarifies an ambiguous v0.9.0 rule, this amendment controls. It MUST NOT be interpreted to broaden authority or weaken a fail-safe requirement.

The governing invariant is:

> **No conforming implementation may produce an affirmative authority or reliance outcome merely because required semantics are absent, incomparable, stale, conflicting, inaccessible, unsupported, non-converged, or ambiguous.**

Machine-readable adversarial vectors are published at `conformance/test-vectors/adversarial-authority-v0.9.1.json` and are release-gated by `scripts/validate_candidate_hardening.py`.

## 1. Monotonic delegation and scope intersection

The effective authority of a downstream delegation MUST be the semantic intersection of the issuer's effective authority and the downstream delegation's declared scope.

For every constrained dimension, a downstream value MUST be proven to denote a semantic subset of the corresponding effective upstream value. The dimensions include, as applicable, action, resource, purpose, jurisdiction, time, quantitative limits, approvals, prohibitions, assurance requirements, subject constraints, deployment constraints, and delegation depth.

Omission of an upstream constraint MUST NOT remove, reset, wildcard, or otherwise broaden that constraint. A downstream delegation that omits a constrained dimension inherits the effective upstream constraint unchanged.

A prohibition MUST be inherited unless the competent upstream authority explicitly defines a narrower prohibition-removal mechanism and the governing profile permits it. A downstream delegation MUST NOT remove a mandatory prohibition merely by omitting it.

Where two scope expressions use different vocabularies, taxonomies, jurisdiction models, resource grammars, or policy languages, the evaluator MUST establish a governed subset relation before treating the downstream expression as narrower. If the subset relation cannot be established, the result MUST be `deny` or `indeterminate`; it MUST NOT be `allow` or `allow_with_conditions`.

The effective delegation operation is therefore:

```text
effective_authority(child) = effective_authority(parent) ∩ child_declared_scope
```

and the intersection MUST be computed monotonically across the complete delegation lineage.

## 2. Temporal interval and clock semantics

Unless a profile explicitly defines a stricter interval, ARPA validity intervals are half-open:

```text
effective_from <= evaluation_time < effective_until
```

A null `effective_until` denotes no declared upper bound; it does not override revocation, suspension, supersession, or another applicable status boundary.

An action evaluated exactly at `effective_until` is outside the interval.

Evaluators MUST normalize timestamps to a common time basis and MUST preserve the original timestamp where required for evidence. Profiles used for consequential action MUST declare permitted clock skew, timestamp precision, and treatment of future-dated observations. A future-dated or clock-ambiguous material status MUST NOT silently produce an affirmative decision.

Where multiple material events have the same wall-clock timestamp, a declared authoritative sequence, checkpoint, or equivalent ordering mechanism MUST determine order. If contradictory events remain unordered after applying the declared ordering mechanism, the affected state MUST be `indeterminate`.

## 3. `not_applicable` is not an authority bypass

`not_applicable` MAY be returned only where the requested operation is outside the declared authority-evaluation domain of the selected profile or policy.

Absence of authority, missing delegation, expired authority, revoked authority, suspended authority, unsupported evidence, unavailable evidence, an unrecognized issuer, an incomparable scope, an unresolved critical extension, stale material state, or an inability to determine authority MUST NOT produce `not_applicable`.

Where authority evaluation is applicable but cannot produce an affirmative determination, the evaluator MUST return `deny` or `indeterminate` according to the applicable policy and reason codes.

## 4. Recognition conflict and issuer competence

A precedence rule MAY establish which source is competent for a particular record type, subject, jurisdiction, or scope. Once a published governance rule establishes that one source is authoritative and another source is non-authoritative for that scope, the lower-precedence statement need not constitute an unresolved authoritative conflict.

Where two or more simultaneously competent authoritative sources conflict and no applicable governance rule removes one source's competence or deterministically resolves the conflict, the evaluator MUST return `deny` or `indeterminate`. It MUST NOT select the most permissive source, retain a cached affirmative result, or reinterpret the conflict as `not_applicable`.

The decision receipt MUST identify the conflicting claims, competence/recognition basis, precedence rule evaluated, and resulting disposition.

## 5. Revocation effectiveness and convergence

An effective authoritative revocation immediately makes the revoked authority non-affirmative for new authority evaluations. From the revocation's effective time, an authority evaluator MUST NOT return `allow` or `allow_with_conditions` for a new action dependent on that authority.

Revocation convergence is a separate enforcement-evidence property. A registry MUST distinguish at least:

- `revoked_propagation_pending`;
- `revoked_propagation_failed`; and
- `revoked_converged`.

Pending or failed enforcement acknowledgement MUST NOT restore or extend revoked authority. It indicates that enforcement evidence is incomplete or that operational containment has failed.

A propagation deadline is an operational bound, not evidence of convergence. Missing required acknowledgements after the deadline MUST produce a propagation failure or escalation state.

## 6. Deterministic evaluation context and checkpoints

A deterministic ARPA decision is a function of the complete evaluation state, not merely a request body and policy identifier.

For consequential authority evaluation, the reproducibility tuple MUST include, directly or by digest/reference:

- request and material context;
- evaluation time;
- policy identifier and version;
- selected authoritative record identifiers and versions/digests;
- material source checkpoints or sequence positions;
- freshness inputs;
- recognition/issuer-competence state; and
- material external evidence used by the policy.

Two evaluations are required to produce the same decision and reason-code set only when this reproducibility tuple is equivalent.

Where a decision depends on multiple independently ordered sources, the decision receipt MUST identify the source checkpoint set sufficient to reconstruct the evaluated snapshot. If no coherent snapshot can be established for material state, the decision MUST be non-affirmative.

## 7. Proof-input semantics

A proof type used for a normative ARPA record MUST define:

- the exact proof input transformation;
- fields excluded from or transformed before proof computation;
- canonicalization or deterministic encoding;
- algorithm and suite identification;
- domain separation or context binding;
- verification-method interpretation;
- key-status evaluation time; and
- replay/context-binding semantics where replay is material.

Use of JCS or another canonicalization algorithm alone does not define which logical object is signed. An implementation MUST NOT claim proof interoperability unless these proof-input semantics are declared and implemented consistently.

Proof validity continues to establish only the claims supported by the proof and configured trust relationship; it MUST NOT establish authority, recognition, assurance, or acceptable reliance by itself.

## 8. Multi-dimensional status composition

Registration, operational, authority, assurance, and security status MUST remain separate dimensions. Cross-dimensional execution gating MUST NOT rely on a single total ordering of heterogeneous status labels.

Each material status dimension MUST map under the applicable profile/policy to one of:

- `permit`;
- `permit_with_conditions`;
- `deny`; or
- `indeterminate`.

Composition MUST be monotonic toward safety:

1. any applicable `deny` yields a non-affirmative result;
2. an applicable `indeterminate` MUST NOT be converted to `permit` merely because another dimension is affirmative;
3. conditions accumulate unless the governing policy explicitly proves that one condition supersedes another; and
4. a less restrictive status in one dimension MUST NOT cancel a more restrictive material status in another dimension.

## 9. Pairwise identity and continuity

A deployment claiming both privacy-preserving scoped identifiers and cross-context continuity MUST define an authorized mechanism for proving the required continuity predicate without exposing a globally reusable correlator.

The mechanism MAY use protected linkage, selective disclosure, commitments, derived pseudonyms, or another governed proof technique. The specification does not mandate a proof construction.

A relying party MUST NOT infer that two pairwise identifiers represent the same logical agent merely from similarity, metadata correlation, operator identity, or network endpoint overlap.

## 10. Schema corrections and authority

A schema-only correction MUST NOT acquire de facto normative authority by changing the set of accepted records contrary to published prose.

A schema version MAY advance without a Candidate document version change only when all of the following are true:

- the prior machine-readable artifact is demonstrably defective;
- the governing prose already unambiguously requires the corrected behavior;
- the defect, rationale, and compatibility impact are recorded;
- the correction does not broaden authority or weaken fail-safe processing; and
- repository conformance evidence demonstrates alignment.

If a proposed schema change alters required fields, field semantics, authority interpretation, lifecycle semantics, decision behavior, or the set of records that the prose permits, the Candidate Specification MUST be versioned accordingly.

## 11. Required adversarial conformance assertions

A v0.9.1 conformance suite for authority evaluation MUST include negative or boundary vectors covering at least:

1. omitted parent constraint;
2. incomparable scope vocabularies;
3. exact expiry boundary;
4. unordered contradictory events at the same timestamp;
5. future-dated material status outside permitted skew;
6. authoritative revocation with pending enforcement convergence;
7. conflicting equally competent authoritative sources;
8. stale affirmative projection versus fresh negative authoritative state;
9. unknown critical extension;
10. proof-valid but incompetent issuer;
11. assurance bound to a different deployment;
12. material change after assurance;
13. pairwise identifier continuity without an authorized linkage proof;
14. unavailable historical evidence;
15. retroactive revocation with and without a competent governance basis;
16. missing delegation incorrectly proposed as `not_applicable`;
17. permissive and restrictive recognized sources with unresolved competence conflict;
18. child delegation dropping an upstream prohibition;
19. child delegation changing to an incomparable constraint vocabulary; and
20. replay of a decision or execution receipt after a material authority boundary changes.

Each adversarial vector MUST identify the expected decision or state, required reason codes, decisions that are prohibited, and the evidence required to explain the result.

## 12. Conformance disposition

An implementation claiming ARPA v0.9.1 authority-evaluator conformance MUST demonstrate that ambiguous or incomplete authority cannot become affirmative solely through omission, parser behavior, precedence defaults, cache behavior, unavailable evidence, or unsupported semantics.

Passing the repository adversarial vectors demonstrates conformance to the modeled cases only. It is not independent certification, formal verification, or proof that an implementation is secure against every adversarial input.
