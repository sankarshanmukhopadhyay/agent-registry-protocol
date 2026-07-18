---
layout: default
title: "Implementation Selection Guide"
nav_exclude: true
---

# Implementation Selection Guide

Select the smallest profile that accurately represents the relying decision. Do not claim a higher profile merely because the implementation can parse its records.

## Decision path

1. **Discovery only:** implement Profile A and ARPA-Core.
2. **Operational accountability without delegated transactions:** add Relations, Assurance and Evidence for Profile B.
3. **Action-specific delegated authority:** add Authority and enforcement integration for Profile C.
4. **Rights-affecting, fiduciary, safety-critical or cross-governance action:** implement Profile D and document independent governance, recognition, revocation convergence and redress evidence.

## Required deployment declaration

Every implementation publishes a Conformance Declaration identifying supported modules, profile, identifier schemes, proof suites, transports, freshness targets, revocation targets and known limitations.

## Fail behaviour

Discovery MAY return stale projections with warnings where policy permits. Authority evaluation MUST return `indeterminate` or `deny` when current status, authority, required assurance or proof validity cannot be established. Missing evidence MUST NOT become an affirmative result.
