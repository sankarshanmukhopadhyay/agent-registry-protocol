from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
required=['README.md','LICENSE','LICENSE-CODE','CHANGELOG.md','ROADMAP.md','GOVERNANCE.md','CONTRIBUTING.md','SECURITY.md','CODE_OF_CONDUCT.md','CITATION.cff','AI_USAGE.md','PORTFOLIO_STATUS.md','docs/index.md','docs/interoperability.md','docs/release-policy.md','spec/arpa-v0.9.0-candidate-specification.md','docs/architecture/trqp-arpa-interoperability.md','docs/candidate-specification-guide.md','docs/migration-v0.5.0-to-v0.9.0.md','RELEASE_NOTES_v0.9.0.md','.github/workflows/validate.yml','.github/workflows/pages.yml','.github/ISSUE_TEMPLATE/bug_report.yml','.github/ISSUE_TEMPLATE/implementation_report.yml','.github/pull_request_template.md']
errors=[]
for rel in required:
    if not (ROOT/rel).exists(): errors.append(f'missing required flagship artifact: {rel}')
for path in list(ROOT.glob('*.md'))+list((ROOT/'docs').glob('*.md')):
    text=path.read_text()
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
        if target.startswith(('http://','https://','#','mailto:')): continue
        clean=target.split('#')[0]
        if clean and not (path.parent/clean).resolve().exists(): errors.append(f'{path.relative_to(ROOT)}: broken local link {target}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('validate_repository.py: flagship baseline and local Markdown links OK')
