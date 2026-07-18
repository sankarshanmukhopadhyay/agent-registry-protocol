---
layout: default
title: "ARPA Proof and Digest Profile"
nav_exclude: true
---

# ARPA Proof and Digest Profile

## Canonical input

For JSON records, the default canonical representation is JCS-compatible deterministic JSON using UTF-8, lexicographically sorted keys and no insignificant whitespace. The `proof` member is excluded from the digest input unless a registered proof suite states otherwise.

## Digest

The v0.5.0 baseline digest is SHA-256 and is serialized as `sha256:<lowercase-hex>`. A digest establishes byte-level commitment to canonical content. It does not establish issuer competence, truth, authority or assurance.

## Proof object

A proof identifies type, verification method, proof purpose, creation time, optional expiry, canonicalization identifier and signature value. Verifiers MUST check record status, issuer competence, key status and critical extensions in addition to cryptographic validity.

## Failure behaviour

Digest mismatch, invalid signature, expired proof, revoked key or unknown critical proof extension produces `ARPA-PROOF-INVALID` or `ARPA-EXT-CRITICAL-UNKNOWN`. High-risk evaluation fails closed.
