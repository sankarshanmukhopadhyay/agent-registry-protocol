#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE="$ROOT/ietf/draft-sankarshan-agent-registry-protocol.md"
OUT="$ROOT/ietf/generated"
BASE="draft-sankarshan-agent-registry-protocol-00"

mkdir -p "$OUT"

if ! command -v kramdown-rfc >/dev/null 2>&1; then
  echo "error: kramdown-rfc is not installed; run 'make ietf-setup'" >&2
  exit 2
fi
if ! command -v xml2rfc >/dev/null 2>&1; then
  echo "error: xml2rfc is not installed; run 'make ietf-setup'" >&2
  exit 2
fi

kramdown-rfc "$SOURCE" > "$OUT/$BASE.xml"
xml2rfc --text --out "$OUT/$BASE.txt" "$OUT/$BASE.xml"
xml2rfc --html --out "$OUT/$BASE.html" "$OUT/$BASE.xml"

echo "Built:"
echo "  ietf/generated/$BASE.xml"
echo "  ietf/generated/$BASE.txt"
echo "  ietf/generated/$BASE.html"
