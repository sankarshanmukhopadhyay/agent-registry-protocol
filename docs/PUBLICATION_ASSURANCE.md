---
layout: default
title: "GitHub Pages Publication Assurance"
nav_exclude: true
---

# GitHub Pages Publication Assurance

The GitHub Pages site is a release artefact of this repository. Publication is permitted only when every source declared in `docs/publication-map.yml` has a deterministic rendered output and the generated site passes internal-link, fragment, asset, base-path, and Mermaid-presence checks.

## Publication authority

The `main` branch is the production documentation authority. Pull requests build and validate the complete site but cannot deploy it. The `pages.yml` workflow deploys only after the same manifest-driven assurance checks succeed.

## Machine-verifiable evidence

Each validation run generates:

- `artifacts/pages/publication-manifest.json`, mapping each publication source to its required output;
- `artifacts/pages/publication-assurance.json`, recording page counts, checked references, Mermaid coverage, and defects;
- the complete `_site` build as the Pages deployment artefact.

A missing rendered page, unresolved Markdown URL, missing local target, invalid heading fragment, missing local asset, or output collision fails the workflow.

## Local validation

```bash
make pages-check
```

This builds the production site under `/agent-registry-protocol`, creates the publication manifest, and validates the generated output.
