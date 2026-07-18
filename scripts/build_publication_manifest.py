#!/usr/bin/env python3
"""Build the authoritative GitHub Pages source-to-output manifest."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import yaml

def output_path(source: str) -> str:
    p=Path(source)
    if p.name == "index.md":
        return str(Path("_site") / p.parent / "index.html")
    return str(Path("_site") / p.with_suffix(".html"))

def has_front_matter(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    return text.startswith("---\n") and "\n---\n" in text[4:]

def title_of(path: Path) -> str:
    text=path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end=text.find("\n---\n",4)
        if end != -1:
            data=yaml.safe_load(text[4:end]) or {}
            if data.get("title"): return str(data["title"])
    match=re.search(r"^#\s+(.+?)\s*$",text,re.M)
    return match.group(1).strip() if match else path.stem

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",default=".")
    ap.add_argument("--map",default="docs/publication-map.yml")
    ap.add_argument("--output",default="artifacts/pages/publication-manifest.json")
    args=ap.parse_args()
    root=Path(args.root)
    spec=yaml.safe_load((root/args.map).read_text(encoding="utf-8"))
    entries=[]; outputs={}
    for item in spec["publication_sources"]:
        source=item["path"]
        src=root/source
        if not src.is_file(): raise SystemExit(f"Publication source does not exist: {source}")
        if item["mode"] == "rendered-page" and not has_front_matter(src):
            raise SystemExit(
                f"Rendered publication source lacks explicit Jekyll front matter: {source}"
            )
        out=output_path(source)
        if out in outputs: raise SystemExit(f"Output collision: {source} and {outputs[out]} -> {out}")
        outputs[out]=source
        entries.append({"source":source,"expected_output":out,"mode":item["mode"],"title":title_of(src)})
    payload={"schema_version":1,"source_count":len(entries),"entries":entries}
    target=root/args.output; target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    print(f"Publication manifest: {len(entries)} rendered-page sources")
    return 0
if __name__ == "__main__": raise SystemExit(main())
