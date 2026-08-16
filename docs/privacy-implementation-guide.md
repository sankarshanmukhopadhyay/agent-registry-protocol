---
layout: default
title: "Privacy Implementation Guide"
nav_exclude: true
---

# Privacy Implementation Guide

ARPA can expose a high-value graph of agents, principals, operators, beneficiaries, delegations, capabilities, incidents and governance relationships. Privacy therefore applies not only to record contents but also to **searchability, graph reconstruction, query telemetry, status probing and historical resolution**.

## Data minimization and disclosure classes

Publish only data required for a relying decision. Keep principals, beneficiaries, confidential delegation terms, detailed evidence and execution records behind authorized resolution. Every deployment should classify records and relationships as public, ecosystem-visible, pairwise/context-scoped, tenant-specific, or confidential according to the sensitivity of the association.

Unauthenticated discovery must return only content explicitly classified for public disclosure. Authenticated access does not itself authorize broader disclosure: policy must bind caller, purpose, audience and retention expectations.

## Correlation controls

Where stable identifiers or public relationships can enable cross-context linkage, use pairwise/context-scoped identifiers or an equivalent anti-correlation mechanism. Avoid publishing edges that reveal beneficiaries, protected professional relationships, sensitive organizational structure, security topology, or confidential commercial associations when a scoped assertion or derived decision is sufficient.

## Query and enumeration privacy

Treat list/search endpoints, status lookups and historical queries as privacy-sensitive surfaces. Apply bounded pagination, rate controls, query minimization and auditable access. Higher-assurance deployments should detect systematic enumeration and distinguish ordinary relying-party resolution from bulk graph extraction.

## Evidence and historical state

Execution receipts should use digests, encrypted references and scoped evidence packages rather than embedding raw protected inputs or outputs. Point-in-time reconstruction must respect retention and legal constraints without erasing the existence of terminal lifecycle events needed for accountability. Access to historical evidence should itself be auditable.

## Deployment evidence

A privacy claim should be backed by a data-flow inventory, disclosure matrix, retention schedule, access-control tests, enumeration-abuse tests and evidence-access logs. Repository conformance proves protocol behavior, not jurisdiction-specific privacy compliance.

See [Governance and Security Assurance](governance-security-assurance.md) and the [2026-08-16 RAHP audit](assurance/rahp-audit-2026-08-16.md).
