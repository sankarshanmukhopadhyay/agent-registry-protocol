---
layout: default
title: "Contributing"
nav_exclude: true
---

# Contributing

Thank you for helping develop the Agent Registry Protocol.

## Contribution principles

Contributions should improve implementability, interoperability, security, privacy, governance clarity, or reviewability. The project values concrete failure modes, precise requirements, testable behavior, and explicit trade-offs over broad aspirational language.

## Public specification review

The Candidate Specification is open to public review. If you identify a normative ambiguity, interoperability problem, governance or authority gap, lifecycle concern, security or privacy risk, conformance issue, missing edge case, or editorial problem, open a **Specification feedback** issue using the repository issue form.

Reviewers do not need to propose a complete solution. A useful issue identifies the affected specification text, explains the concern and its impact, and includes evidence or an example where available. Specification feedback is an input to project governance; opening an issue does not by itself modify the normative baseline.

## Before opening a pull request

For substantive protocol changes, open an issue first. Describe:

1. the problem or failure mode;
2. the affected actors, records, processing rules, or conformance profiles;
3. the proposed normative change;
4. backward-compatibility and migration effects;
5. security and privacy implications;
6. federation or governance implications; and
7. proposed tests or examples.

Editorial corrections that do not alter semantics may be submitted directly.

## Normative language

Use **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** only when defining interoperable behavior or conformance expectations. Explain the rationale near consequential requirements.

## Pull-request expectations

A pull request should:

- have a focused scope;
- reference the relevant issue;
- update the changelog for material changes;
- include examples or test vectors where behavior changes;
- preserve section numbering and internal links;
- distinguish normative requirements from rationale and implementation guidance;
- pass repository validation; and
- avoid claiming standards-body endorsement.

## Review dimensions

Reviewers should consider:

- conceptual correctness;
- protocol determinism;
- independent implementability;
- security and abuse resistance;
- privacy and data minimization;
- operational feasibility;
- governance legitimacy and contestability;
- backward compatibility; and
- testability.

## Commit messages

Use concise, imperative commit titles. Recommended prefixes include:

- `spec:` normative specification changes
- `docs:` explanatory documentation
- `schema:` machine-readable schemas
- `test:` conformance tests and vectors
- `security:` threat model or control changes
- `governance:` project or protocol governance changes
- `ci:` repository automation
- `chore:` maintenance without semantic change

## Licensing of contributions

By submitting a contribution, you agree that the repository uses artifact-specific licensing:

- normative and informative specification text, documentation, diagrams, narrative examples, governance prose, and release-note content are contributed under **CC BY 4.0**; and
- source code, scripts, reference implementations, executable validators, machine-readable schemas, OpenAPI/AsyncAPI contracts, test vectors, fixtures, machine-readable mappings, executable configuration, and generated machine-readable evidence are contributed under **Apache-2.0**.

The deterministic classification map is maintained in `licensing/artifact-license-policy.json`. A file-level license notice, if present, takes precedence for that file.

You certify that you have the right to submit the contribution under these terms.

## Conduct

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Normative change checklist

Substantial proposals must identify:

- the authority or governance actor competent to make the change;
- affected modules and profiles;
- schema and protocol-contract updates;
- positive, negative and indeterminate test cases;
- security, privacy and revocation consequences;
- compatibility and migration effects;
- documentation and implementation-report effects.
