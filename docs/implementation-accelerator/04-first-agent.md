---
layout: default
title: "Your first agent"
parent: "Implementation Accelerator"
nav_order: 4
---
# Your first agent

The canonical sample agent is `agentreg:acme.example:procurement-review`. It is intentionally small enough to understand while retaining the control-plane links required for meaningful governance.

## Lifecycle exercised

1. create the immutable canonical identifier;
2. attach governance, service and relationship records;
3. publish current lifecycle status;
4. resolve the complete record set;
5. inspect emitted registration and update events.

Run `make pilot-seed`, then use the commands in `implementation-accelerator/http/quickstart.http` or the Postman/Insomnia collections.
