#!/usr/bin/env python3
from __future__ import annotations
import json, os, sys
from pathlib import Path
from datetime import datetime, timezone
import httpx

BASE=os.getenv("ARPA_BASE_URL","http://localhost:8000").rstrip("/")
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts"/"pilot"/"pilot-readiness-report.json"
AGENT="agentreg:acme.example:procurement-review"
checks=[]
def check(name, fn):
    try:
        detail=fn(); checks.append({"name":name,"status":"pass","detail":detail})
    except Exception as e:
        checks.append({"name":name,"status":"fail","detail":str(e)})

def get(path):
    r=httpx.get(BASE+path,timeout=10); r.raise_for_status(); return r.json()
def post(path,payload):
    r=httpx.post(BASE+path,json=payload,timeout=10); r.raise_for_status(); return r.json()

check("health",lambda: get("/health")["status"])
check("registry_metadata",lambda: get("/registry")["registry_id"])
check("agent_resolution",lambda: get("/agents/"+AGENT)["agent"]["agent_id"])
check("agent_status",lambda: get("/agents/"+AGENT+"/status")["registration"])
check("alias_resolution",lambda: get("/aliases/acme:procurement-review")["canonical_id"])
allow=json.loads((ROOT/"implementation-accelerator/requests/authority-allow.json").read_text())
deny=json.loads((ROOT/"implementation-accelerator/requests/authority-deny.json").read_text())
check("authority_allow",lambda: post("/authority/evaluate",allow)["decision"])
check("authority_deny",lambda: post("/authority/evaluate",deny)["decision"])
check("events",lambda: len(get("/events")["events"]))
for f in sorted((ROOT/"implementation-accelerator/fixtures/acme").glob("*.json")):
    check("fixture:"+f.name,lambda f=f: json.loads(f.read_text()).get("record_id"))
ready=all(c["status"]=="pass" for c in checks)
report={"release":"0.9.1","generated_at":datetime.now(timezone.utc).isoformat(),"base_url":BASE,"decision":"ready" if ready else "not_ready","checks":checks,"limitations":["Reference implementation only","Human governance and security checklists require accountable sign-off"]}
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
sys.exit(0 if ready else 1)
