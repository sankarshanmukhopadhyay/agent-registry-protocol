#!/usr/bin/env python3
from pathlib import Path
import json, os, sys
import httpx

base=os.getenv("ARPA_BASE_URL","http://localhost:8000").rstrip("/")
fixture_dir=Path(__file__).resolve().parents[1]/"fixtures"/"acme"
order=["agent-core.json","status.json","governance.json","service-endpoint.json","identifier-alias.json","authority-envelope.json"]
for name in order:
    payload=json.loads((fixture_dir/name).read_text())
    endpoint="/agents" if payload.get("record_type")=="agent_core" else "/records"
    response=httpx.post(base+endpoint,json=payload,timeout=10)
    if response.status_code not in (200,201,409):
        print(f"FAIL {name}: {response.status_code} {response.text}",file=sys.stderr); sys.exit(1)
    print(f"OK   {name}: {response.status_code}")
print("Acme pilot registry loaded")
