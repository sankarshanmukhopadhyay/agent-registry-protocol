from pathlib import Path
import json, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
errors=[]
required=['spec/agent-registry-protocol-v0.9.0.md','docs/architecture/trqp-arpa-interoperability.md','mappings/trqp-arpa-query-projection.yaml','conformance/trqp-projection/manifest.json','independent_impl/projection.py']
for r in required:
 if not (ROOT/r).exists(): errors.append('missing candidate artifact: '+r)
m=yaml.safe_load((ROOT/'mappings/trqp-arpa-query-projection.yaml').read_text())
for kind in ('authorization','recognition'):
 for item in m['mappings'][kind]:
  for field in ('target','source_artifact','source_field','transform','cardinality','preconditions','failure_outcome','evidence','information_loss'):
   if field not in item: errors.append(f'mapping {kind}/{item.get("target","?")} missing {field}')
states=set(m['state_projection']); expected={'active','suspended','revoked','expired','unknown','conflicting','unavailable'}
if states!=expected: errors.append('state projection mismatch')
manifest=json.loads((ROOT/'conformance/trqp-projection/manifest.json').read_text())
if len(manifest['vectors'])<13: errors.append('insufficient TRQP projection vectors')
for x in manifest['vectors']:
 if not (ROOT/'conformance/trqp-projection'/x['path']).exists(): errors.append('missing vector '+x['path'])
if errors:
 print('\n'.join(errors))
 sys.exit(1)
print(f'validate_candidate.py: mapping complete; {len(manifest["vectors"])} projection vectors present')
