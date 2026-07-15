# ARPA Reference Service

This FastAPI service demonstrates ARPA-Core resolution, aliases, events, point-in-time record filtering and the scoped ARPA-Authority evaluator. It is intentionally local-first and not production-ready.

Run with `make run`; API documentation is available at `/docs`. State is in memory unless `ARPA_DB` points to a SQLite file.
