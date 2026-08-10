#!/usr/bin/env python3
"""Validate the ARPA A2A v1.0 mapping, publication model, compatibility rules and conformance vectors."""
from __future__ import annotations
import json
from pathlib import Path
import sys
from datetime import datetime, timezone
import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'conformance/test-vectors/a2a-v1.0'
errors=[]

mapping=yaml.safe_load((ROOT/'mappings/a2a-v1.0-arpa-mapping.yaml').read_text())
if mapping.get('profile')!='https://arpa.example/profiles/a2a/1.0': errors.append('mapping profile identifier is incorrect')
if mapping.get('precedence',{}).get('authoritative_arpa_state_over_card') is not True: errors.append('mapping does not preserve ARPA state precedence')
if mapping.get('safe_failure',{}).get('authority_indeterminate')!='reject_consequential_action': errors.append('mapping does not fail closed on indeterminate authority')
pub=mapping.get('registry_publication',{})
if not pub.get('exact_source_uri_required') or pub.get('authority_implication') is not False: errors.append('publication invariants missing')

for schema_name in ['a2a-publication-projection.schema.json','a2a-card-compatibility-result.schema.json']:
    schema=json.loads((ROOT/'schemas'/schema_name).read_text())
    Draft202012Validator.check_schema(schema)

manifest=json.loads((BASE/'manifest.json').read_text())
known_errors={e['id'] for e in json.loads((ROOT/'registries/error-codes.json').read_text())['entries']}

def compatibility(v):
    removed=v.get('removed',[])
    breaking_prefixes=('skills:','interfaces:','securitySchemes:','inputModes:','outputModes:')
    if any(x.startswith(breaking_prefixes) for x in removed) or v.get('disabled_capability'): return 'breaking'
    return 'compatible'

def evaluate(v):
    case=v['case']
    if case=='digest-mismatch' and not v['arpa']['digest_match']: return 'reject','ARPA-A2A-CARD-DIGEST-MISMATCH'
    if case=='unsupported-required-extension' and not v['arpa']['required_extensions_supported']: return 'reject','ARPA-A2A-REQUIRED-EXTENSION-UNSUPPORTED'
    if case=='status-conflict' and v['arpa']['agent_status']!='active': return 'reject','ARPA-A2A-CARD-STATUS-CONFLICT'
    if case=='missing-authority' and v['arpa']['authority_decision']!='permit': return 'reject','ARPA-A2A-TASK-AUTHORITY-MISSING'
    if case=='task-receipt':
        a=v['a2a']; ok=(v['arpa']['authority_decision']=='permit' and a.get('task_id') and a.get('context_id') and a.get('artifact_digests'))
        return ('accept',None) if ok else ('reject','ARPA-A2A-ARTIFACT-DIGEST-MISSING')
    if case=='public-card':
        c=v['card']; a=v['arpa']; ok=(c.get('protocolVersion')=='1.0' and c.get('interfaces') and a.get('digest_match') and a.get('agent_status')=='active' and a.get('deployment_status')=='active')
        return ('accept',None) if ok else ('reject','ARPA-A2A-INTERFACE-UNRECOGNISED')
    if case=='publication':
        p=v['publication']
        if p.get('agent_card_uri')!=p.get('source_uri'): return 'reject','ARPA-A2A-PUBLICATION-URI-MISMATCH'
        if p.get('used_for_consequential_decision') and not p.get('snapshot_preserved'): return 'reject','ARPA-A2A-SNAPSHOT-MISSING'
        if p.get('authority_implication') is not False: return 'reject','ARPA-A2A-TASK-AUTHORITY-MISSING'
        return ('accept',None) if p.get('digest_match') else ('reject','ARPA-A2A-CARD-DIGEST-MISMATCH')
    if case=='visibility':
        ok = (v.get('returned') is False) if not v.get('caller_authorized') and v.get('disclosure_class')!='public' else True
        return ('accept',None) if ok else ('reject','ARPA-ID-NOT-AUTHORIZED')
    if case=='compatibility':
        actual=compatibility(v)
        return ('accept',None) if actual==v.get('expected_classification') else ('reject','ARPA-STATE-TRANSITION-INVALID')
    if case=='non-implication':
        ok=v.get('authority_decision')!='permit' and v.get('invocation_allowed') is False
        return ('accept',None) if ok else ('reject','ARPA-A2A-TASK-AUTHORITY-MISSING')
    if case=='precedence':
        ok=v.get('arpa_status')!='active' and v.get('invocation_allowed') is False
        return ('accept',None) if ok else ('reject','ARPA-A2A-CARD-STATUS-CONFLICT')
    return 'reject','ARPA-A2A-VERSION-UNSUPPORTED'

passed=0; results=[]
for item in manifest['vectors']:
    v=json.loads((BASE/item['file']).read_text())
    decision,error=evaluate(v)
    ok=decision==item['expected'] and error==item.get('error')
    if item.get('error') and item['error'] not in known_errors:
        ok=False; errors.append(f"{item['id']}: unregistered error code {item['error']}")
    print(f"[{'OK' if ok else 'FAIL'}] {item['id']} {item['file']}: {decision}{' '+error if error else ''}")
    results.append({'id':item['id'],'file':item['file'],'passed':ok,'decision':decision,'error':error})
    if ok: passed+=1
    else: errors.append(f"{item['id']}: expected {item['expected']} {item.get('error')}, got {decision} {error}")

outdir=ROOT/'artifacts/interoperability'; outdir.mkdir(parents=True,exist_ok=True)
report={'profile':mapping['profile'],'implementation_release':'0.9.3','generated_at':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'passed':passed,'total':len(manifest['vectors']),'results':results}
(outdir/'a2a-registry-report.json').write_text(json.dumps(report,indent=2)+"\n")
bundle={'type':'arpa-a2a-registry-evidence-bundle','implementation_release':'0.9.3','report':'artifacts/interoperability/a2a-registry-report.json','mapping':'mappings/a2a-v1.0-arpa-mapping.yaml','publication_schema':'schemas/a2a-publication-projection.schema.json','compatibility_schema':'schemas/a2a-card-compatibility-result.schema.json','vector_manifest':'conformance/test-vectors/a2a-v1.0/manifest.json','invariants':['exact-source-uri','caller-filtered-visibility','immutable-snapshot','discovery-not-authority','arpa-state-precedence']}
(outdir/'a2a-registry-evidence-bundle.json').write_text(json.dumps(bundle,indent=2)+"\n")

print(f"validate_a2a_interoperability.py: {passed}/{len(manifest['vectors'])} OK")
if errors:
    print('\n'.join(errors)); sys.exit(1)
