#!/usr/bin/env python3
"""Validate complete GitHub Pages rendering, links, fragments, and assets."""
from __future__ import annotations
import argparse, json, re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ATTRS=("href","src")
class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs=[]
        self.ids=set()
        self.title_count=0
        self.mermaid_blocks=0
        self._head_depth=0

    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=="head":
            self._head_depth += 1
        elif tag=="title" and self._head_depth:
            # Count only the document title in <head>. SVG diagrams and icons
            # may legitimately contain their own <title> accessibility nodes.
            self.title_count += 1
        classes=set((d.get("class") or "").split())
        if tag in {"code", "pre", "div"} and "language-mermaid" in classes:
            self.mermaid_blocks += 1
        for key in ("id","name"):
            if d.get(key): self.ids.add(d[key])
        for key in ATTRS:
            if d.get(key): self.refs.append((key,d[key]))

    def handle_endtag(self,tag):
        if tag=="head" and self._head_depth:
            self._head_depth -= 1

def page_for_url(site:Path, current:Path, path:str, baseurl:str)->Path:
    path=unquote(path)
    if path.startswith(baseurl+"/"): path=path[len(baseurl):]
    elif path==baseurl: path="/"
    if path.startswith("/"): candidate=site/path.lstrip("/")
    else: candidate=current.parent/path
    if candidate.is_dir(): candidate=candidate/"index.html"
    elif candidate.suffix=="":
        html=candidate.with_suffix(".html")
        candidate=html if html.exists() else candidate/"index.html"
    return candidate.resolve()

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--manifest",default="artifacts/pages/publication-manifest.json"); ap.add_argument("--site",default="_site"); ap.add_argument("--baseurl",default="/agent-registry-protocol"); ap.add_argument("--report",default="artifacts/pages/publication-assurance.json")
    a=ap.parse_args(); site=Path(a.site).resolve(); manifest=json.loads(Path(a.manifest).read_text())
    errors=[]; html_files=sorted(site.rglob("*.html")); parsed={}
    for e in manifest["entries"]:
        target=Path(e["expected_output"]).resolve()
        if not target.is_file(): errors.append(f"Missing rendered page: {e['source']} -> {e['expected_output']}")
    for f in html_files:
        p=Parser(); p.feed(f.read_text(encoding="utf-8",errors="replace")); parsed[f.resolve()]=p
        if p.title_count != 1: errors.append(f"Expected one HTML title element in {f}, found {p.title_count}")
    checked=0; fragments=0; assets=0
    for current,p in parsed.items():
        for kind,raw in p.refs:
            if raw.startswith(("mailto:","tel:","javascript:","data:")): continue
            u=urlsplit(raw)
            if u.scheme or u.netloc: continue
            if not u.path and not u.fragment: continue
            checked+=1
            if re.search(r"\.md$",u.path,re.I): errors.append(f"Unresolved Markdown link in {current.relative_to(site)}: {raw}")
            target=page_for_url(site,current,u.path or current.name,a.baseurl)
            if not target.exists(): errors.append(f"Missing local target in {current.relative_to(site)}: {raw} -> {target}"); continue
            if kind=="src": assets+=1
            if u.fragment and target.suffix.lower()==".html":
                fragments+=1; tp=parsed.get(target)
                if tp is None:
                    q=Parser(); q.feed(target.read_text(encoding="utf-8",errors="replace")); parsed[target]=q; tp=q
                if unquote(u.fragment) not in tp.ids: errors.append(f"Missing fragment in {current.relative_to(site)}: {raw}")
    mermaid_pages=sum(1 for parser in parsed.values() if parser.mermaid_blocks)
    report={"schema_version":1,"source_pages":manifest["source_count"],"rendered_html_pages":len(html_files),"internal_references_checked":checked,"fragment_references_checked":fragments,"local_assets_checked":assets,"mermaid_pages":mermaid_pages,"errors":errors}
    out=Path(a.report); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k!="errors"},indent=2))
    if errors:
        print("\nPublication validation failures:")
        for x in errors: print(f"- {x}")
        return 1
    print("Publication assurance: PASS")
    return 0
if __name__=="__main__": raise SystemExit(main())
