---
layout: default
title: "Identifier Resolution Guide"
nav_exclude: true
---

# Identifier Resolution Guide

Resolution returns one of: `active_record`, `terminal_record`, `not_found`, `not_authorized`, `conflict` or `indeterminate`.

1. Parse and normalize the identifier.
2. Locate the registry authority.
3. Resolve canonical records before aliases.
4. Verify alias issuer competence, validity and status.
5. Detect loops and conflicting active aliases.
6. Resolve point-in-time state when `at` is supplied.
7. Return source and freshness metadata.

Never-issued identifiers return `not_found`. Known terminal identifiers return their historical terminal record. Access-controlled records return `not_authorized` without disclosing protected content.
