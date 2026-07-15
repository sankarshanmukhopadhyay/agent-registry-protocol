from pathlib import Path
import json
import sys
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []

for path in sorted((ROOT / 'schemas').glob('*.json')):
    try:
        Draft202012Validator.check_schema(json.loads(path.read_text()))
    except Exception as exc:
        errors.append(f'{path}: {exc}')

for path in sorted((ROOT / 'registries').glob('*.json')):
    try:
        data = json.loads(path.read_text())
        assert data['entries']
        ids = [entry['id'] for entry in data['entries']]
        assert len(ids) == len(set(ids))
    except Exception as exc:
        errors.append(f'{path}: {exc}')

for path in (ROOT / 'openapi/arpa-openapi.yaml', ROOT / 'asyncapi/arpa-events.yaml'):
    try:
        yaml.safe_load(path.read_text())
    except Exception as exc:
        errors.append(f'{path}: {exc}')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print('validate_artifacts.py: schemas, registries and YAML parsed successfully')
