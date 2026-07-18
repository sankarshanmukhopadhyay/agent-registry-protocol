---
layout: default
title: "15-minute quickstart"
parent: "Implementation Accelerator"
nav_order: 1
---
# 15-minute quickstart

## Objective

Start the reference registry, load a governed sample agent and prove that resolution and authority evaluation work.

## Prerequisites

- Docker with Compose v2
- `curl`
- Python 3.10+ for evidence validation

## 1. Start the registry

```bash
make pilot-up
```

Wait until the health check returns `ok`:

```bash
curl --fail http://localhost:8000/health
```

## 2. Load the canonical sample registry

```bash
make pilot-seed
```

The loader creates Acme Corporation's registry entry, agent core record, lifecycle status, service endpoint, governance record, relationships and identifier alias.

## 3. Resolve the first agent

```bash
curl --fail   http://localhost:8000/agents/agentreg:acme.example:procurement-review
```

Expected evidence:

- canonical identifier is returned;
- the agent core record is present;
- linked governance and relationship records are included;
- response declares authoritative resolution.

## 4. Evaluate delegated authority

```bash
curl --fail -X POST http://localhost:8000/authority/evaluate   -H 'content-type: application/json'   --data @implementation-accelerator/requests/authority-allow.json
```

The result must include a decision, reason codes and a durable decision receipt.

## 5. Generate pilot evidence

```bash
make pilot-check
```

This writes:

```text
artifacts/pilot/pilot-readiness-report.json
```

A successful report contains `"decision": "ready"`.

## 6. Stop the environment

```bash
make pilot-down
```

## Completion criteria

| Gate | Required result |
|---|---|
| Health | HTTP 200 and `status=ok` |
| Metadata | Registry advertises ARPA v0.9.0 and implementation release v0.9.1 |
| Registration | Agent core accepted |
| Resolution | Canonical agent resolves with linked records |
| Authority | Decision receipt returned |
| Evidence | Pilot report says `ready` |
