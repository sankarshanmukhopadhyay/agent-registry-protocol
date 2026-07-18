---
layout: default
title: "API consumer toolkit"
parent: "Implementation Accelerator"
nav_order: 10
---
# API consumer toolkit

The accelerator provides four equivalent entry points:

- generated FastAPI Swagger UI at `http://localhost:8000/docs`;
- `implementation-accelerator/http/quickstart.http` for IDE HTTP clients;
- `implementation-accelerator/postman/ARPA-v0.9.1.postman_collection.json`;
- `implementation-accelerator/insomnia/ARPA-v0.9.1-insomnia.json`.

The normative API contract remains `openapi/arpa-openapi.yaml`. Accelerator collections are convenience artefacts and must be regenerated or reviewed when the OpenAPI contract changes.
