---
layout: default
title: "Quickstart"
nav_exclude: true
---

# Quickstart

> This path validates and runs the reference implementation locally. For a pilot registry with retained evidence, use the [15-minute quickstart](implementation-accelerator/01-15-minute-quickstart.md). For a complete release gate, use the [Candidate Specification implementation guide](candidate-specification-guide.md). Compare all journeys in [Start Here](start-here.md).

## Local validation

```bash
make setup
make validate
make test
```

## Run the reference service

```bash
make run
```

The service listens on `http://127.0.0.1:8000`. Retrieve registry metadata:

```bash
curl http://127.0.0.1:8000/registry
```

Register the example agent:

```bash
curl -X POST http://127.0.0.1:8000/agents \
  -H 'Content-Type: application/json' \
  --data @examples/valid/agent-core.json
```

Resolve it:

```bash
curl http://127.0.0.1:8000/agents/agentreg:example.org:agent-123
```

The reference service is an interoperability aid, not a production deployment or trust certification service.
