# Interoperability Harness

This directory contains two separately configured registry fixtures and a deterministic exchange harness for ARPA v0.5.0.

- `fixtures/registry-alpha/` acts as the authoritative publisher.
- `fixtures/registry-beta/` acts as a recognising registry and relying enforcement point.
- `policy/portable-policy.json` is evaluated by two adapters.
- `scripts/run_interoperability.py` generates the report and evidence bundle.

The fixtures demonstrate protocol interoperability, not independent organisational implementations.
