---
layout: default
title: "Security Deployment Guide"
nav_exclude: true
---

# Security Deployment Guide

Threats include alias hijacking, confused-deputy use, unauthorized relationship issuance, projection poisoning, replay, stale status, event gaps, key compromise, transfer abuse, malicious extensions, privacy leakage, authority expansion, registry enumeration, governance capture, recovery abuse, federation conflict and revocation convergence failure.

High-risk deployments fail closed when current authority, security status, required assurance or proof validity cannot be established. Unknown critical extensions are rejected. Every material status transition is signed, time-stamped, scoped and delivered to enforcement subscribers with acknowledgement or a disclosed maximum propagation time.

## Administrative compromise

Separate high-impact administration from routine registry operation. Profile C/D deployments require independent multi-party authorization for the operations enumerated in Candidate Specification §29.3. Administrative authorization should be transaction-intent bound so approvers can verify subject, affected records, effective time, downstream effects and policy basis before approval.

## Revocation convergence

Do not equate publication of a revocation event with completed enforcement. Track the required enforcement-point set, acknowledgement state, propagation deadline and unresolved failures. A missing required acknowledgement leaves convergence incomplete and must remain visible to relying policy.

## Federation and recognition

Technical federation is not recognition. Recognition withdrawal must invalidate future affirmative reliance under that recognition rule, subject to explicit historical-effect semantics. Conflicting authoritative status without an applicable precedence rule is indeterminate or stricter; never select the permissive source by default.

## Recovery after compromise

Recovery is a privileged control plane. Restoration after confirmed compromise requires fresh security evidence plus independent authorization appropriate to the profile. The actor or key suspected in the compromise must not be sufficient by itself to authorize restoration.

## Discovery privacy and abuse resistance

Unauthenticated discovery exposes only explicitly public projections. Apply bounded pagination, rate controls and monitoring for enumeration patterns, and avoid leaking private or tenant-specific existence through search filters or error behavior where policy requires indistinguishability.

Run `python3 scripts/validate_governance_assurance.py` to exercise the repository-owned negative vectors for these controls.
