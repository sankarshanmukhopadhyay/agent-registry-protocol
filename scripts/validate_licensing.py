from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

required = [
    "LICENSE",
    "LICENSE-CONTENT",
    "LICENSE-CODE",
    "NOTICE",
    "licensing/artifact-license-policy.json",
]
for rel in required:
    if not (ROOT / rel).exists():
        errors.append(f"missing licensing artifact: {rel}")

if not errors:
    root_license = (ROOT / "LICENSE").read_text()
    if "CC-BY-4.0" not in root_license or "Apache-2.0" not in root_license:
        errors.append("LICENSE must identify both CC-BY-4.0 and Apache-2.0")

    content = (ROOT / "LICENSE-CONTENT").read_text()
    if "Creative Commons Attribution 4.0 International" not in content:
        errors.append("LICENSE-CONTENT does not identify CC BY 4.0")

    code = (ROOT / "LICENSE-CODE").read_text()
    if "Apache License" not in code or "Version 2.0" not in code:
        errors.append("LICENSE-CODE does not contain Apache License 2.0")

    policy = json.loads((ROOT / "licensing/artifact-license-policy.json").read_text())
    licenses = policy.get("licenses", {})
    if licenses.get("content", {}).get("spdx") != "CC-BY-4.0":
        errors.append("artifact license policy content SPDX must be CC-BY-4.0")
    if licenses.get("software", {}).get("spdx") != "Apache-2.0":
        errors.append("artifact license policy software SPDX must be Apache-2.0")

    readme = (ROOT / "README.md").read_text()
    for token in ("LICENSE-CONTENT", "LICENSE-CODE", "artifact-license-policy.json"):
        if token not in readme:
            errors.append(f"README licensing section missing {token}")

    citation = (ROOT / "CITATION.cff").read_text()
    if "type: software" in citation and "license: Apache-2.0" not in citation:
        errors.append("CITATION.cff software citation must identify Apache-2.0")
    if "license: CC-BY-4.0" in citation:
        errors.append("CITATION.cff must not describe the software release as CC-BY-4.0")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("validate_licensing.py: artifact-specific licensing map OK")
