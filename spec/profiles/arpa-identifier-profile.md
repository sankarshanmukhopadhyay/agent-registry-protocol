---
layout: default
title: "ARPA Identifier and Alias Profile"
nav_exclude: true
---

# ARPA Identifier and Alias Profile

## 1. Canonical syntax

```abnf
agentreg-uri = "agentreg:" registry-authority ":" agent-local-id
registry-authority = 1*( ALPHA / DIGIT / "." / "-" )
agent-local-id = 1*( unreserved / pct-encoded / sub-delims / ":" )
unreserved = ALPHA / DIGIT / "-" / "." / "_" / "~"
pct-encoded = "%" HEXDIG HEXDIG
sub-delims = "!" / "$" / "&" / "'" / "(" / ")" / "*" / "+" / "," / ";" / "="
```

The scheme and registry authority are compared case-insensitively. The local identifier is case-sensitive. Percent-encoded octets representing unreserved characters MUST be normalized to their unencoded form. Other percent encodings use uppercase hexadecimal.

## 2. Persistence

A canonical identifier MUST NOT be reassigned to a semantically different agent. Retirement, revocation and supersession preserve historical resolution.

## 3. Aliases

An alias is a separately issued, statused and time-bounded claim. It MUST identify its binding type and competent issuer. Supported binding types are `equivalent_subject`, `implementation_anchor`, `legacy_identifier` and `service_identifier`.

Alias resolution MUST detect loops, conflicting active bindings and unauthorized issuers. A conflict produces `indeterminate`, not silent precedence.

## 4. Ownership and storage identifiers

A ledger token, database key, DID, CAIP identifier or URN MAY be an alias or implementation anchor. Possession or transfer of that identifier MUST NOT silently transfer ARPA authority, assurance or accountability records.
