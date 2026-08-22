#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "interop" / "tga-agentic-governance-alignment.json"
data = json.loads(path.read_text())
errors = []

if data.get("relationship") != "informative-implementation-alignment":
    errors.append("TGA relationship must remain informative implementation alignment")
if data.get("semanticAuthority") != "trust-systems-meta-model":
    errors.append("TSMM must remain semantic authority")
if data.get("portableContractAuthority") != "trust-infrastructure-schemas":
    errors.append("TIS must remain portable contract authority")
if data.get("authorityBoundary", {}).get("nonDependency") is not True:
    errors.append("alignment must explicitly remain non-dependent")
required_modules = {"ARPA-Core", "ARPA-Relations", "ARPA-Assurance", "ARPA-Authority", "ARPA-Evidence", "ARPA-Federation"}
missing = sorted(required_modules - set(data.get("moduleMappings", {})))
if missing:
    errors.append("missing ARPA module mappings: " + ", ".join(missing))
required_rules = {
    "identity != authority",
    "capability != permission",
    "registration != authority",
    "relationship != delegated_authority",
    "technical_federation != governance_recognition"
}
missing_rules = sorted(required_rules - set(data.get("nonImplications", [])))
if missing_rules:
    errors.append("missing non-implication rules: " + ", ".join(missing_rules))
if "execution_success != legitimate_effect" not in data.get("nonImplications", []):
    errors.append("execution success must not imply legitimate effect")
if len(data.get("guideResponsibilitiesOutsideArpa", [])) < 5:
    errors.append("alignment must retain explicit responsibilities outside ARPA")

doc = ROOT / "docs" / "architecture" / "tga-agentic-governance-alignment.md"
if not doc.exists():
    errors.append("missing reciprocal architecture documentation")
else:
    text = doc.read_text()
    for term in ["identity does not imply authority", "technical federation does not imply governance recognition", "complete agentic runtime"]:
        if term.lower() not in text.lower():
            errors.append(f"architecture documentation missing boundary signal: {term}")

if errors:
    print("TGA alignment validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)
print(f"TGA alignment validation passed ({len(data.get('moduleMappings', {}))} ARPA modules mapped).")
