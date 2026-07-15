# Quickstart

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
