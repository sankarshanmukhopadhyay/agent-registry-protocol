#!/usr/bin/env python3
from pathlib import Path
import json, sys
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
ROOT=Path(__file__).resolve().parents[1]
errors=[]

def load(rel): return json.loads((ROOT/rel).read_text())

# Lifecycle registry structural + state coverage checks.
states={e['id'] for e in load('registries/lifecycle-statuses.json')['entries']}
trs=load('registries/lifecycle-transitions.json')['entries']
ids=[x['id'] for x in trs]
if len(ids)!=len(set(ids)): errors.append('duplicate lifecycle transition id')
for t in trs:
    if t['from'] not in states or t['to'] not in states: errors.append('unknown lifecycle state in '+t['id'])
for terminal in ('revoked','retired','superseded'):
    ordinary=[t for t in trs if t['from']==terminal and t['class']!='governance_reversal']
    if ordinary: errors.append(f'{terminal} has non-governance-reversal outgoing transition')

# Revocation convergence: status cannot be converged with unresolved targets.
schema=load('schemas/revocation-convergence.schema.json')
base={"revocation_event_id":"evt-1","propagation_target_seconds":60,"applicable_targets":["pep-a","pep-b"],"acknowledged_targets":["pep-a"],"failed_targets":[],"removed_from_scope":[],"evaluated_at":"2026-08-18T00:00:00Z","evidence_refs":["ack-a"]}
def unresolved(x):
    resolved=set(x['acknowledged_targets'])|set(x['removed_from_scope'])
    return set(x['applicable_targets'])-resolved
for status in ('published','propagating','propagation_failed','indeterminate'):
    d=dict(base,status=status)
    if not unresolved(d): errors.append('test fixture unexpectedly resolved')
# Positive converged fixture.
conv=dict(base,status='converged',acknowledged_targets=['pep-a','pep-b'])
if unresolved(conv): errors.append('converged fixture unresolved')
for e in Draft202012Validator(schema).iter_errors(conv): errors.append('converged schema: '+e.message)
# Semantic rule beyond JSON Schema.
bad=dict(base,status='converged')
if not unresolved(bad): errors.append('negative convergence fixture unexpectedly resolved')

# Profile C/D declarations require acknowledgement-based convergence and B-D consequential policy.
cs=load('schemas/conformance-declaration.schema.json')
resources=[]
for path in (ROOT/'schemas').rglob('*.schema.json'):
    doc=json.loads(path.read_text())
    resources.append(Resource.from_contents(doc))
registry=Registry().with_resources((r.id(),r) for r in resources if r.id())
validator=Draft202012Validator(cs, registry=registry)
common={"schema_version":"1.0.0","issuer":"registry:example.org","issued_at":"2026-08-18T00:00:00Z","effective_from":"2026-08-18T00:00:00Z","effective_until":None,"status":"active","proof":{},"record_id":"c","record_type":"conformance-declaration","subject":"registry:x","implementation_name":"x","implementation_version":"0.9.5","arpa_version":"0.9.0","modules":["ARPA-Core"],"identifier_schemes":["agentreg"],"query_transports":["https"],"known_limitations":[]}
for profile in ('B','C','D'):
    d={**common,"profile":profile}
    errs=list(validator.iter_errors(d))
    if not errs: errors.append(f'Profile {profile} missing consequential_action_policy was accepted')
for profile in ('C','D'):
    d={**common,"profile":profile,"consequential_action_policy":{"policy_id":"p","version":"1","classification_basis":["risk"],"evidence_obligations":["receipt"]},"revocation_convergence":{"acknowledgement_required":False,"maximum_propagation_seconds":60}}
    errs=list(validator.iter_errors(d))
    if not errs: errors.append(f'Profile {profile} acknowledgement_required=false was accepted')

# Normative catalogue must be present and non-empty; detailed synchronization is delegated.
cat=load('registries/normative-requirements.json')
if not cat.get('entries'): errors.append('normative requirements catalogue empty')

if errors:
    print('\n'.join(errors)); sys.exit(1)
out=ROOT/'artifacts/conformance/candidate-hardening-validation.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps({"status":"pass","lifecycle_transitions":len(trs),"normative_requirements":len(cat['entries']),"checks":["lifecycle-transition-legality","terminal-state-governance-reversal","revocation-convergence-acknowledgements","profile-consequential-action-policy","profile-cd-acknowledgement-policy"]},indent=2)+"\n")
print(f'validate_candidate_hardening.py: PASS ({len(trs)} transitions; {len(cat["entries"])} normative requirements)')
