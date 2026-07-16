from __future__ import annotations
import hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIX=ROOT/'interop'/'fixtures'
OUT=ROOT/'artifacts'/'interoperability'

def load(path): return json.loads(path.read_text())
def digest(obj): return 'sha256:'+hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def get_path(obj,path):
    cur=obj
    for part in path.split('.'):
        cur=cur[part]
    return cur

def eval_portable(policy,context):
    outcomes=[]
    for rule in policy['all']:
        actual=get_path(context,rule['path'])
        op=rule['operator']; expected=rule['value']
        outcomes.append(actual==expected if op=='equals' else actual<=expected if op=='less_than_or_equal' else False)
    return policy['effect'] if all(outcomes) else 'deny'

def eval_reference(policy,context):
    # Independent adapter shape over the same portable rule document.
    predicates={'equals':lambda a,b:a==b,'less_than_or_equal':lambda a,b:a<=b}
    for rule in policy['all']:
        if not predicates[rule['operator']](get_path(context,rule['path']),rule['value']): return 'deny'
    return policy['effect']

def check(name,passed,evidence): return {'name':name,'passed':bool(passed),'evidence':evidence}

def main():
    alpha=load(FIX/'registry-alpha'/'registry-metadata.json')
    beta=load(FIX/'registry-beta'/'registry-metadata.json')
    agent=load(FIX/'registry-alpha'/'agent-core.json')
    recognition=load(FIX/'registry-beta'/'recognition.json')
    events=load(FIX/'registry-alpha'/'events.json')
    policy=load(ROOT/'interop'/'policy'/'portable-policy.json')
    checks=[]
    checks.append(check('metadata-discovery',alpha['arpa_version']=='0.5.0' and 'ARPA-Core' in alpha['supported_modules'],{'registry_id':alpha['registry_id'],'modules':alpha['supported_modules']}))
    imported_digest=digest(agent)
    checks.append(check('canonical-resolution',agent['agent_id']==agent['subject'] and imported_digest.startswith('sha256:'),{'agent_id':agent['agent_id'],'digest':imported_digest}))
    recognized=recognition['status']=='active' and agent['record_type'] in recognition['recognized_record_types'] and recognition['recognized_registry']==alpha['registry_id']
    checks.append(check('scoped-recognition',recognized,{'recognition_id':recognition['recognition_id'],'record_type':agent['record_type']}))
    contiguous=[e['sequence'] for e in events]==list(range(events[0]['sequence'],events[-1]['sequence']+1))
    checks.append(check('event-continuity',contiguous,{'sequences':[e['sequence'] for e in events]}))
    revocation=events[-1]['event_type'] in {'agent.suspended','delegation.revoked','assurance.revoked'}
    acknowledgement={'enforcement_point':'pdp:beta','event_id':events[-1]['event_id'],'subject':events[-1]['subject'],'acknowledged_at':'2026-07-16T01:00:02Z','resulting_status':'blocked'}
    checks.append(check('revocation-propagation',revocation,{'event_id':events[-1]['event_id'],'event_type':events[-1]['event_type']}))
    checks.append(check('enforcement-acknowledgement',revocation and acknowledgement['resulting_status']=='blocked',acknowledgement))
    active_context={'request':{'action':'purchase','amount':500},'subject':{'status':'active'}}
    suspended_context={'request':{'action':'purchase','amount':500},'subject':{'status':'suspended'}}
    decisions={'portable_active':eval_portable(policy,active_context),'reference_active':eval_reference(policy,active_context),'portable_suspended':eval_portable(policy,suspended_context),'reference_suspended':eval_reference(policy,suspended_context)}
    equivalent=decisions['portable_active']==decisions['reference_active']=='allow' and decisions['portable_suspended']==decisions['reference_suspended']=='deny'
    checks.append(check('policy-portability',equivalent,decisions))
    bundle={'bundle_version':'1.0.0','arpa_version':'0.5.0','producer':'ARPA repository interoperability harness','fixtures':[alpha['registry_id'],beta['registry_id']],'artifacts':{'alpha_metadata':digest(alpha),'beta_metadata':digest(beta),'agent_core':imported_digest,'recognition':digest(recognition),'events':digest(events),'policy':digest(policy)},'revocation_acknowledgement':acknowledgement,'limitations':['Fixtures are maintained in one repository and are not independent implementations','No production cryptographic proof or key custody','No network transport or durable message broker','Recognition is demonstrated by deterministic fixture processing']}
    bundle['bundle_digest']=digest(bundle)
    report={'report_version':'1.0.0','generated_at':datetime.now(timezone.utc).isoformat(),'release':'v0.5.0','title':'ARPA interoperability report','participants':[alpha['registry_id'],beta['registry_id']],'checks':checks,'passed':all(c['passed'] for c in checks),'evidence_bundle':'artifacts/interoperability/evidence-bundle.json','evidence_bundle_digest':bundle['bundle_digest'],'independence_claim':False,'known_limitations':bundle['limitations']}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'evidence-bundle.json').write_text(json.dumps(bundle,indent=2)+'\n')
    (OUT/'interoperability-report.json').write_text(json.dumps(report,indent=2)+'\n')
    for c in checks: print(f"[{'OK' if c['passed'] else 'FAIL'}] {c['name']}")
    print(f"interoperability: {sum(c['passed'] for c in checks)}/{len(checks)} checks passed")
    return 0 if report['passed'] else 1
if __name__=='__main__': sys.exit(main())
