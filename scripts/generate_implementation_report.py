from pathlib import Path
import datetime
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
checks = []
for name, command in [
    ('examples', ['python3', 'scripts/validate_examples.py']),
    ('vectors', ['python3', 'scripts/validate_test_vectors.py']),
    ('extended-vectors', ['python3', 'scripts/validate_extended_vectors.py']),
    ('artifacts', ['python3', 'scripts/validate_artifacts.py']),
    ('repository', ['python3', 'scripts/validate_repository.py']),
    ('interoperability', ['python3', 'scripts/run_interoperability.py']),
    ('tests', ['python3', '-m', 'pytest', '-q']),
]:
    process = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    checks.append({
        'name': name,
        'passed': process.returncode == 0,
        'output': (process.stdout + process.stderr)[-4000:],
    })

report = {
    'report_version': '1.0.0',
    'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'implementation': 'ARPA reference service',
    'implementation_version': '0.5.0',
    'arpa_version': '0.5.0',
    'modules': ['ARPA-Core', 'ARPA-Relations', 'ARPA-Authority', 'ARPA-Evidence'],
    'profile_claims': ['A', 'C-demonstration-only'],
    'checks': checks,
    'passed': all(check['passed'] for check in checks),
    'known_limitations': [
        'No production key custody',
        'No independent identity proofing',
        'No distributed consensus',
        'No production federation service',
        'Repository interoperability fixtures are not independent implementations',
        'Authority evaluator supports the deterministic reference policy subset',
    ],
}
out = ROOT / 'conformance/reports/reference-implementation-report.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2) + '\n')
print(out)
raise SystemExit(0 if report['passed'] else 1)
