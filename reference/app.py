from __future__ import annotations
import hashlib, json, os, uuid
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from .storage import Store
from scripts.reference_evaluator import evaluate_authority

app=FastAPI(title='ARPA Reference Service',version='0.4.0')
store=Store(os.getenv('ARPA_DB',':memory:'))

def now(): return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def problem(status,code,title,detail='',reasons=None,retryable=False):
    return JSONResponse(status_code=status,content={'type':f'https://arpa.example/problems/{code.lower()}','title':title,'status':status,'code':code,'detail':detail,'correlation_id':str(uuid.uuid4()),'reason_codes':reasons or [],'retryable':retryable})
def emit(subject,event_type,payload=None):
    event={'event_id':str(uuid.uuid4()),'event_type':event_type,'subject':subject,'source':'registry:reference','effective_at':now(),'issued_at':now(),'payload':payload or {}}
    event['sequence']=store.add_event(event); return event

@app.get('/health')
def health(): return {'status':'ok','version':'0.4.0'}

@app.get('/registry')
def registry():
    return {'registry_id':'registry:reference','name':'ARPA Reference Registry','arpa_version':'0.4.0','supported_modules':['ARPA-Core','ARPA-Relations','ARPA-Authority','ARPA-Evidence'],'supported_profiles':['A','C'],'authoritative_base_uri':'http://127.0.0.1:8000','conformance_declaration_uri':'http://127.0.0.1:8000/records/conformance-reference','event_retention_seconds':86400,'status_max_age_seconds':300}

@app.post('/agents',status_code=201)
def register_agent(record:dict):
    aid=record.get('agent_id') or record.get('subject')
    if not isinstance(aid,str) or not aid.startswith('agentreg:'): raise HTTPException(422,'agent_id must use agentreg scheme')
    existing=store.records_for_subject(aid)
    if any(r.get('record_type')=='agent_core' for r in existing): return problem(409,'ARPA-STATE-TRANSITION-INVALID','Identifier already issued','Canonical identifiers are non-reassignable')
    store.put_record(record); emit(aid,'agent.registered',{'record_id':record['record_id']}); return record

@app.post('/records',status_code=201)
def put_record(record:dict):
    store.put_record(record)
    subject=record.get('agent_id') or record.get('subject')
    if record.get('record_type')=='identifier-alias': store.add_alias(record); emit(subject,'alias.added',{'alias':record['alias']})
    else: emit(subject if isinstance(subject,str) else record['record_id'],'agent.metadata.updated',{'record_id':record['record_id'],'record_type':record['record_type']})
    return record

@app.get('/records/{record_id}')
def get_record(record_id:str):
    r=store.get_record(record_id)
    if not r: return problem(404,'ARPA-ID-NOT-FOUND','Record not found')
    return r

@app.get('/agents/{agent_id}')
def resolve_agent(agent_id:str,at:str|None=Query(None)):
    records=store.records_for_subject(agent_id,at)
    core=[r for r in records if r.get('record_type')=='agent_core']
    if not core: return problem(404,'ARPA-ID-NOT-FOUND','Agent not found','Identifier was never issued or is not visible')
    return {'agent':core[-1],'records':records,'resolution_time':now(),'at':at,'authoritativeness':'authoritative','projection_lag_seconds':0}

@app.get('/agents/{agent_id}/status')
def get_status(agent_id:str,at:str|None=Query(None)):
    records=store.records_for_subject(agent_id,at)
    statuses=[r for r in records if r.get('record_type')=='status']
    if not statuses: return problem(409,'ARPA-AUTHORITY-INDETERMINATE','Status unavailable',retryable=True)
    return statuses[-1]

@app.get('/agents/{agent_id}/events')
def agent_events(agent_id:str,after:int=0): return {'events':store.events(agent_id,after),'after':after}
@app.get('/events')
def events(after:int=0): return {'events':store.events(None,after),'after':after}

@app.get('/aliases/{alias:path}')
def resolve_alias(alias:str,at:str|None=Query(None)):
    instant=at or now(); matches=store.resolve_alias(alias,instant)
    if not matches: return problem(404,'ARPA-ID-NOT-FOUND','Alias not found')
    ids=sorted({r['canonical_id'] for r in matches})
    if len(ids)>1: return problem(409,'ARPA-ID-CONFLICT','Alias conflict','Multiple active canonical identifiers', ['alias_conflict'])
    return {'alias':alias,'canonical_id':ids[0],'records':matches,'at':instant}

@app.post('/authority/evaluate')
def authority_evaluate(payload:dict):
    decision,reasons=evaluate_authority(payload)
    receipt={'record_id':str(uuid.uuid4()),'record_type':'decision-receipt','schema_version':'1.0.0','issuer':'pdp:reference','subject':payload.get('request',{}).get('agent','unknown'),'issued_at':now(),'effective_from':now(),'effective_until':None,'status':'issued','request_digest':'sha256:'+hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'decision':decision,'reason_codes':reasons,'evaluator':'pdp:reference','policy_version':'reference-0.4.0'}
    store.put_record(receipt)
    return {'decision':decision,'reason_codes':reasons,'decision_receipt':receipt}

@app.post('/reliance/evaluate')
def reliance_evaluate(payload:dict):
    required=payload.get('required_modules',[]); supported=set(registry()['supported_modules']); missing=[m for m in required if m not in supported]
    if missing: return {'decision':'indeterminate','reason_codes':['required_module_not_supported'],'missing_modules':missing}
    return {'decision':'allow','reason_codes':['required_modules_supported']}
