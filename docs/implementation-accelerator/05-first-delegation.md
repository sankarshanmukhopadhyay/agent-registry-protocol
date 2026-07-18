---
layout: default
title: "Your first delegation"
parent: "Implementation Accelerator"
nav_order: 5
---
# Your first delegation

The sample delegation authorizes the procurement-review agent to evaluate bounded purchase requests but not submit transactions or transfer funds.

```mermaid
flowchart TD
  ACME[Acme Corporation] --> REG[Procurement registrar]
  REG --> AGENT[Procurement review agent]
  AGENT --> ALLOW[Review purchase request]
  AGENT -. prohibited .-> DENY[Submit payment]
```

## Required pilot evidence

- an allow decision for an in-scope review request;
- a deny decision for a prohibited transaction request;
- receipts linked to the exact request digest;
- policy version and evaluator identity;
- event or audit retention sufficient for later review.
