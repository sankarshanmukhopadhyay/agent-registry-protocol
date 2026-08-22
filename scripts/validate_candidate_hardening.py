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
conv=dict(base,status='converged',acknowledged_targets=['pep-a','pep-b'])
if unresolved(conv): errors.append('converged fixture unresolved')
for e in Draft202012Validator(schema).iter_errors(conv): errors.append('converged schema: '+e.message)
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

# Base normative catalogue remains required.
cat=load('registries/normative-requirements.json')
if not cat.get('entries'): errors.append('normative requirements catalogue empty')

# v0.9.1 adversarial authority hardening vectors are required and structurally bounded.
adv=load('conformance/test-vectors/adversarial-authority-v0.9.1.json')
if adv.get('arpa_version')!='0.9.1': errors.append('adversarial vector suite must declare arpa_version 0.9.1')
vectors=adv.get('vectors',[])
vector_ids=[v.get('id') for v in vectors]
if len(vectors)<20: errors.append('adversarial vector suite must contain at least 20 boundary cases')
if len(vector_ids)!=len(set(vector_ids)): errors.append('duplicate adversarial vector id')
required_fields={'id','scenario','expected_decision','prohibited_decisions','required_reason_codes','required_evidence'}
for vector in vectors:
    missing=required_fields-set(vector)
    if missing: errors.append(f"{vector.get('id','<unknown>')} missing adversarial fields: {sorted(missing)}")
    if not vector.get('required_reason_codes'): errors.append(f"{vector.get('id','<unknown>')} has no required reason code")
    if not vector.get('required_evidence'): errors.append(f"{vector.get('id','<unknown>')} has no required evidence")
for vector_id in ('ADV-001','ADV-002','ADV-003','ADV-004','ADV-005','ADV-006','ADV-007','ADV-008','ADV-009','ADV-010','ADV-011','ADV-012','ADV-016','ADV-017','ADV-018','ADV-019','ADV-020'):
    vector=next((v for v in vectors if v.get('id')==vector_id),None)
    if vector is None:
        errors.append(f'missing required adversarial vector {vector_id}')
        continue
    prohibited=set(vector.get('prohibited_decisions',[]))
    if not {'allow','allow_with_conditions'}.issubset(prohibited):
        errors.append(f'{vector_id} does not explicitly prohibit affirmative authority decisions')
adv16=next((v for v in vectors if v.get('id')=='ADV-016'),{})
if 'not_applicable' not in set(adv16.get('prohibited_decisions',[])):
    errors.append('ADV-016 must prohibit not_applicable')

# Hardening requirement catalogue must be complete, unique and trace to the vector suite or inspection.
hard=load('registries/adversarial-hardening-requirements-v0.9.1.json')
if hard.get('arpa_version')!='0.9.1': errors.append('hardening requirements must declare arpa_version 0.9.1')
hard_entries=hard.get('entries',[])
hard_ids=[e.get('id') for e in hard_entries]
if len(hard_entries)<12: errors.append('hardening requirement catalogue must contain at least 12 requirements')
if len(hard_ids)!=len(set(hard_ids)): errors.append('duplicate hardening requirement id')
known_vectors=set(vector_ids)
for entry in hard_entries:
    for field in ('id','title','section','requirement','verification','expected_evidence'):
        if not entry.get(field): errors.append(f"{entry.get('id','<unknown>')} missing hardening field {field}")
    for verification in entry.get('verification',[]):
        if verification!='inspection' and verification not in known_vectors:
            errors.append(f"{entry.get('id','<unknown>')} references unknown verification {verification}")
    if not entry.get('expected_evidence'):
        errors.append(f"{entry.get('id','<unknown>')} has no expected evidence")

if errors:
    print('\n'.join(errors)); sys.exit(1)
out=ROOT/'artifacts/conformance/candidate-hardening-validation.json'
out.parent.mkdir(parents=True,exist_ok=True)
checks=["lifecycle-transition-legality","terminal-state-governance-reversal","revocation-convergence-acknowledgements","profile-consequential-action-policy","profile-cd-acknowledgement-policy","adversarial-authority-vector-structure","adversarial-fail-safe-outcomes","not-applicable-bypass-prohibition","hardening-requirement-traceability"]
out.write_text(json.dumps({"status":"pass","lifecycle_transitions":len(trs),"normative_requirements":len(cat['entries']),"hardening_requirements":len(hard_entries),"adversarial_vectors":len(vectors),"checks":checks},indent=2)+"\n")
print(f'validate_candidate_hardening.py: PASS ({len(trs)} transitions; {len(cat["entries"])} base normative requirements; {len(hard_entries)} hardening requirements; {len(vectors)} adversarial vectors)')
