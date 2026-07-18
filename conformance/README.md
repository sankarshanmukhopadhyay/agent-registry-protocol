---
layout: default
title: "Conformance"
nav_exclude: true
---

# Conformance

ARPA conformance is evidence-based across six dimensions: protocol, semantic, cryptographic, operational, governance and enforcement.

- `profiles/` defines Profiles A-D.
- `test-vectors/TV-*` contains the original profile decision vectors.
- `test-vectors/extended/` covers digests, issuer competence, transfer effects, event gaps, aliases, multi-hop delegation, recognition withdrawal and appeal restoration.
- `reports/` contains the implementation-report schema, template and generated reference report.

Run:

```bash
python3 scripts/validate_test_vectors.py
python3 scripts/validate_extended_vectors.py
python3 scripts/generate_implementation_report.py
```

Passing schemas alone is not full ARPA conformance. Implementations must identify unsupported dimensions and operational limitations.
