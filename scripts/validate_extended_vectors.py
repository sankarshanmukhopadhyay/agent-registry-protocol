from pathlib import Path
import json, sys
from governance_checks import canonical_digest, issuer_competent, transfer_outcomes, detect_event_gap, resolve_alias_graph, delegation_chain_valid, recognition_effective, lifecycle_transition_allowed
ROOT=Path(__file__).resolve().parents[1]
passed=0; total=0
for path in sorted((ROOT/'conformance/test-vectors/extended').glob('*.json')):
    total+=1; vector=json.loads(path.read_text()); kind=vector['kind']; data=vector['input']; expected=vector['expected']
    if kind=='digest': actual=canonical_digest(data['document'],set(data.get('excluded',['proof'])))
    elif kind=='issuer_competence': actual=issuer_competent(data['relationship_type'],data['issuer_role'])
    elif kind=='transfer': actual=transfer_outcomes(data['assertions'],data.get('explicit_novations',[]))
    elif kind=='event_gap': actual=detect_event_gap(data['sequences'])
    elif kind=='alias_graph': actual=list(resolve_alias_graph(data['start'],data['bindings']))
    elif kind=='delegation_chain': actual=list(delegation_chain_valid(data['chain']))
    elif kind=='recognition': actual=list(recognition_effective(data['status'],data['at'],data.get('effective_until')))
    elif kind=='lifecycle_transition': actual=lifecycle_transition_allowed(data['prior'],data['new'])
    else: actual='unsupported-kind'
    ok=actual==expected
    print(f"[{'OK' if ok else 'FAIL'}] {vector['id']}: {kind}")
    if not ok: print(' expected=',expected,'actual=',actual)
    passed+=int(ok)
print(f'validate_extended_vectors.py: {passed}/{total} OK')
sys.exit(0 if passed==total else 1)
