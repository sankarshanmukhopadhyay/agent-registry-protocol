#!/usr/bin/env python3
"""Validate ARPA documentation navigation and catalogue assurance.

This check complements validate_publication.py. It validates generated-page
reachability, curated journey depth, required Start Here links, and direct
catalogue coverage of normative/profile-normative artifacts.
"""
from __future__ import annotations
import argparse, collections, json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if tag == 'a' and d.get('href'): self.refs.append(d['href'])

def resolve(site: Path, current: Path, href: str, baseurl: str) -> Path | None:
    u=urlsplit(href)
    if u.scheme or u.netloc or href.startswith(('mailto:','tel:','javascript:','data:')):
        return None
    path=unquote(u.path)
    if not path: return current
    if path == baseurl: path='/'
    elif path.startswith(baseurl + '/'): path=path[len(baseurl):]
    if path.startswith('/'): target=site/path.lstrip('/')
    else: target=current.parent/path
    if target.is_dir(): target=target/'index.html'
    elif target.suffix == '':
        h=target.with_suffix('.html'); target=h if h.exists() else target/'index.html'
    return target.resolve()

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--site', default='_site')
    ap.add_argument('--manifest', default='artifacts/pages/publication-manifest.json')
    ap.add_argument('--baseurl', default='/agent-registry-protocol')
    ap.add_argument('--report', default='artifacts/pages/docs-link-validation.json')
    ap.add_argument('--max-hops', type=int, default=4)
    args=ap.parse_args()
    site=Path(args.site).resolve()
    manifest=json.loads(Path(args.manifest).read_text())
    html_files={p.resolve() for p in site.rglob('*.html')}
    graph=collections.defaultdict(set)
    errors=[]
    for page in html_files:
        parser=Parser(); parser.feed(page.read_text(encoding='utf-8', errors='replace'))
        for href in parser.refs:
            target=resolve(site,page,href,args.baseurl)
            if target is not None and target in html_files: graph[page].add(target)

    home=(site/'index.html').resolve(); docs=(site/'docs/index.html').resolve(); start=(site/'docs/start-here/index.html').resolve()
    for required in (home,docs,start):
        if required not in html_files: errors.append(f'Missing navigation entry page: {required.relative_to(site)}')

    # Multi-source breadth-first reachability from home and catalogue.
    depths={}
    q=collections.deque()
    for source in (home,docs):
        if source in html_files: depths[source]=0; q.append(source)
    while q:
        current=q.popleft()
        for target in graph[current]:
            if target not in depths:
                depths[target]=depths[current]+1; q.append(target)

    expected=[]
    for entry in manifest['entries']:
        target=Path(entry['expected_output']).resolve()
        if target.suffix.lower()=='.html': expected.append(target)
    unreachable=[p for p in expected if p not in depths]
    too_deep=[p for p in expected if p in depths and depths[p] > args.max_hops]
    for p in unreachable: errors.append(f'Published page is unreachable from home/catalogue: {p.relative_to(site)}')
    for p in too_deep: errors.append(f'Published page exceeds {args.max_hops} navigation hops: {p.relative_to(site)} (depth {depths[p]})')

    # Curated journey links must be direct from Start Here.
    curated=[
      site/'docs/protocol-modules.html', site/'docs/quickstart.html',
      site/'docs/implementation-accelerator/01-15-minute-quickstart.html',
      site/'docs/candidate-specification-guide.html', site/'docs/conformance-guide.html',
      site/'spec/profiles/arpa-a2a-v1.0-interoperability-profile.html'
    ]
    direct=graph.get(start,set())
    for p in map(Path.resolve,curated):
        if p not in direct: errors.append(f'Start Here does not directly link required journey: {p.relative_to(site)}')

    # Normative/profile artifacts must be directly catalogued.
    catalogue=graph.get(docs,set())
    normative=[(site/'spec/agent-registry-protocol-v0.9.0.html').resolve()]
    normative += sorted((site/'spec/profiles').glob('*.html'))
    normative += sorted((site/'conformance/profiles').glob('*.html'))
    for p in normative:
        if p not in catalogue: errors.append(f'Normative/profile page missing from docs catalogue: {p.relative_to(site)}')

    report={
      'schema_version':1,
      'generated_html_pages':len(html_files),
      'manifest_html_pages':len(expected),
      'reachable_manifest_pages':len(expected)-len(unreachable),
      'unreachable_pages':[str(p.relative_to(site)) for p in unreachable],
      'pages_beyond_max_hops':[{'page':str(p.relative_to(site)),'depth':depths[p]} for p in too_deep],
      'max_hops':args.max_hops,
      'required_journeys':len(curated),
      'normative_catalogue_pages':len(normative),
      'errors':errors,
    }
    out=Path(args.report); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('errors','unreachable_pages','pages_beyond_max_hops')},indent=2))
    if errors:
        print('\nDocumentation navigation failures:')
        for e in errors: print(f'- {e}')
        return 1
    print('Documentation navigation assurance: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
