---
layout: default
title: "Portfolio Status"
nav_exclude: true
---

# Portfolio Status

The portfolio repository owns inclusion and strategic tier. This repository owns the project status dimensions declared in [`PROJECT-STATUS.yaml`](PROJECT-STATUS.yaml).

| Attribute | Value | Authority |
|---|---|---|
| Portfolio disposition | Included | Portfolio repository |
| Portfolio tier | Flagship | Portfolio repository |
| Maturity | Pilot ready | `PROJECT-STATUS.yaml` |
| Lifecycle | Active | `PROJECT-STATUS.yaml` |
| Operational status | Active validation | `PROJECT-STATUS.yaml` |
| Specification status | Community Draft | `PROJECT-STATUS.yaml` |
| Current implementation release | v0.9.4 | Repository release history |
| Normative specification surface | v0.9.0 Candidate Specification document | Repository specification |
| Validation | `make release-check` and `make pages-check` | `PROJECT-STATUS.yaml` |
| Candidate evidence | `artifacts/candidate-specification/evidence-bundle.json` | Repository validation |
| Interoperability evidence | `artifacts/interoperability/evidence-bundle.json` | Repository validation |
| Historical-resolution evidence | `artifacts/historical-resolution/evidence-bundle.json` | Repository validation |

ARPA's machine-readable declaration intentionally does not assert formal standards status, certification, independent assurance, legal recognition, or production security approval.

Promotion beyond the current maturity requires external reproduction, independent implementation evidence, resolution of high-severity findings, production experience for durable events and key management, and evidence that the normative surface no longer requires material change.
