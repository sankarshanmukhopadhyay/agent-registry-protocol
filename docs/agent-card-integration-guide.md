---
layout: default
title: "Agent Card Integration Guide"
nav_exclude: true
---

# Agent Card Integration Guide

Use cards for discovery and routing, not as an authorization source. Store or expose an Agent Description Reference containing the card URI, media type, canonicalization method and digest. Map card skills to Capability Declarations with `claim_class: self_declared`. Link independent tests through Capability Verification records and permissions through Authority Envelopes.

A consumer should display identity integrity, capability verification, authority and runtime status as separate signals. A single “verified agent” badge obscures these distinctions and is not an ARPA conformance claim.
