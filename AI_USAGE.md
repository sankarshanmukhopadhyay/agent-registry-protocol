---
layout: default
title: "AI Usage Disclosure"
nav_exclude: true
---

# AI Usage Disclosure

## Purpose

This file records how artificial-intelligence tools may be used in the development and maintenance of the Agent Registry Protocol (ARPA) repository. It supports provenance, review accountability, and reproducible assurance without assigning authority to an AI system.

## Governing rule

AI tools may assist with drafting, restructuring, consistency analysis, test generation, schema review, and documentation maintenance. They do not hold maintainer authority, approve normative changes, establish protocol semantics, or replace human review.

All accepted changes remain attributable to the human contributor and reviewer who submits or merges them.

## Permitted uses

- drafting or restructuring non-normative documentation;
- proposing tests, examples, schemas, and validation logic;
- identifying inconsistencies, broken references, or coverage gaps;
- summarising issue, review, and release context;
- generating candidate implementation code subject to normal review and testing.

## Required controls

AI-assisted contributions MUST:

1. be reviewed for technical accuracy, security impact, licensing, and repository scope;
2. pass the same automated validation and conformance gates as other contributions;
3. avoid introducing unverifiable citations, fabricated implementation evidence, or undisclosed external dependencies;
4. preserve the distinction between normative requirements, examples, and editorial guidance;
5. identify material AI assistance in the pull request when it affected normative text, executable artifacts, or security-relevant code.

## Prohibited authority claims

AI-generated output MUST NOT be treated as:

- evidence of interoperability or conformance;
- approval by a standards body, governance authority, maintainer, implementer, or affected community;
- an independent implementation;
- a security review, legal opinion, or assurance conclusion;
- a substitute for provenance, authorship, or accountable decision-making.

## Disclosure format

For material assistance, use the following pull-request note:

```text
AI assistance: <tool or model, if known>
Scope: <files or work performed>
Human verification: <review and validation completed>
Limitations: <known uncertainties or excluded reliance>
```

## Repository record

The v0.5.0 interoperability release used AI assistance to inspect the repository baseline, propose documentation and validation improvements, implement candidate interoperability fixtures and scripts, and prepare release metadata. The resulting artifacts were validated through repository automation; the maintainer remains responsible for review, acceptance, publication, and any claims made from the release.
