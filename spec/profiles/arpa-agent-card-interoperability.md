# ARPA Agent Card Interoperability Profile

## 1. Scope

This profile maps an external agent-description card into ARPA without making that format normative for ARPA-Core.

## 2. Claim classification

Imported `name`, `description`, `version`, provider metadata, endpoints, security declarations and skills are self-declared unless a competent independent issuer provides linked verification evidence.

A skill or capability in a card MUST NOT be interpreted as capability verification, capability authorization, delegated authority or assurance.

## 3. ARPA extension

The `extensions.arpa` object MAY contain the canonical agent identifier, description digest, and endpoints for status, relationships, assurance, authority and governance. Critical fields MUST be declared in `critical`.

## 4. Integrity processing

A resolver MUST retrieve the exact representation identified by the Agent Description Reference, canonicalize it using the declared method, compute the declared digest and reject a mismatch. A successful check proves integrity relative to the commitment only.

## 5. Conflict handling

Where a card conflicts with an authoritative ARPA record, the resolver MUST identify the conflict and apply relying-party policy. It MUST NOT silently elevate card content over authoritative registry state.
