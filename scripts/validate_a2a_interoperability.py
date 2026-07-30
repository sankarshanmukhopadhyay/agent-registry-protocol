#!/usr/bin/env python3
"""Validate the ARPA A2A v1.0 mapping, schemas and conformance vectors."""
from __future__ import annotations
import json
from pathlib import Path
import sys
import yaml

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'conformance/test-vectors/a2a-v1.0'
errors=[]

mapping=yaml.safe_load((ROOT/'mappings/a2a-v1.0-arpa-mapping.yaml').read_text())
if mapping.get('profile')!='https://arpa.example/profiles/a2a/1.0':
    errors.append('mapping profile identifier is incorrect')
if mapping.get('precedence',{}).get('authoritative_arpa_state_over_card') is not True:
    errors.append('mapping does not preserve ARPA state precedence')
if mapping.get('safe_failure',{}).get('authority_indeterminate')!='reject_consequential_action':
    errors.append('mapping does not fail closed on indeterminate authority')

manifest=json.loads((BASE/'manifest.json').read_text())
known_errors={e['id'] for e in json.loads((ROOT/'registries/error-codes.json').read_text())['entries']}

def evaluate(v):
    case=v['case']
    if case=='digest-mismatch' and not v['arpa']['digest_match']:
        return 'reject','ARPA-A2A-CARD-DIGEST-MISMATCH'
    if case=='unsupported-required-extension' and not v['arpa']['required_extensions_supported']:
        return 'reject','ARPA-A2A-REQUIRED-EXTENSION-UNSUPPORTED'
    if case=='status-conflict' and v['arpa']['agent_status']!='active':
        return 'reject','ARPA-A2A-CARD-STATUS-CONFLICT'
    if case=='missing-authority' and v['arpa']['authority_decision']!='permit':
        return 'reject','ARPA-A2A-TASK-AUTHORITY-MISSING'
    if case=='task-receipt':
        a=v['a2a']; ok=(v['arpa']['authority_decision']=='permit' and a.get('task_id') and a.get('context_id') and a.get('artifact_digests'))
        return ('accept',None) if ok else ('reject','ARPA-A2A-ARTIFACT-DIGEST-MISSING')
    if case=='public-card':
        c=v['card']; a=v['arpa']; ok=(c.get('protocolVersion')=='1.0' and c.get('interfaces') and a.get('digest_match') and a.get('agent_status')=='active' and a.get('deployment_status')=='active')
        return ('accept',None) if ok else ('reject','ARPA-A2A-INTERFACE-UNRECOGNISED')
    return 'reject','ARPA-A2A-VERSION-UNSUPPORTED'

passed=0
for item in manifest['vectors']:
    v=json.loads((BASE/item['file']).read_text())
    decision,error=evaluate(v)
    ok=decision==item['expected'] and error==item.get('error')
    if item.get('error') and item['error'] not in known_errors:
        ok=False; errors.append(f"{item['id']}: unregistered error code {item['error']}")
    print(f"[{'OK' if ok else 'FAIL'}] {item['id']} {item['file']}: {decision}{' '+error if error else ''}")
    if ok: passed+=1
    else: errors.append(f"{item['id']}: expected {item['expected']} {item.get('error')}, got {decision} {error}")

print(f"validate_a2a_interoperability.py: {passed}/{len(manifest['vectors'])} OK")
if errors:
    print('\n'.join(errors)); sys.exit(1)
