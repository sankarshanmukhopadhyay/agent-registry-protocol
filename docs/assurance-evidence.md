---
layout: default
title: Assurance Evidence
---

# Assurance evidence contract

This repository treats repository-native GitHub Actions evidence as the authoritative execution record for portfolio assurance.

| Claim | Required control | Freshness expectation |
|---|---|---|
| Protocol validation | `.github/workflows/validate.yml` | Successful execution covering the governed `main` revision |
| Publication integrity | `.github/workflows/pages.yml` | Successful execution covering the governed `main` revision |
| IETF renderability | `.github/workflows/pages.yml` | Optional; successful Internet-Draft build inside the publication workflow |

A green workflow is evidence for the claim exercised by that workflow; it is not evidence for unrelated claims.

Portfolio finding lineage: `PF-BBBFBF98E2F9`, `PF-CEAD5F9F9FAA` (issue #13).

## Retest rule

After a governed `main` revision completes both required workflows successfully, rerun the Portfolio Assurance Monitor. Close the remediation only when the monitor lifecycle records both fingerprints as resolved.
