---
layout: default
title: "Candidate Specification implementation guide"
nav_exclude: true
---

# Candidate Specification implementation guide

## Reading paths

**Architects:** candidate specification → authority model → ARPA–TRQP architecture → federation and lifecycle evidence.  
**Implementers:** schemas and APIs → mapping contract → adapters → vectors → implementation report.  
**Assurance reviewers:** requirements map → validation reports → compatibility matrix → limitations → evidence bundle.

## One-command validation

```bash
make setup
make release-check
```

The release gate validates schemas, original profiles, repository quality, Candidate Specification artifacts, projection vectors, independent adapter equivalence, networked discovery, durable event replay and retained evidence.
