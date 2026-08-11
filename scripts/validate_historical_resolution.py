from pathlib import Path
import json, sys
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/historical-resolution.schema.json"
VECTOR_DIR = ROOT / "conformance/test-vectors/historical"
ARTIFACT_DIR = ROOT / "artifacts/historical-resolution"

schema = json.loads(SCHEMA_PATH.read_text())
status_schema = json.loads((ROOT / "schemas/status.schema.json").read_text())
registry = Registry().with_resource(status_schema["$id"], Resource.from_contents(status_schema))
validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
manifest = json.loads((VECTOR_DIR / "manifest.json").read_text())
errors = []
results = []

for vector in manifest["vectors"]:
    path = VECTOR_DIR / vector["path"]
    if not path.exists():
        errors.append(f"missing historical vector: {vector['path']}")
        continue
    data = json.loads(path.read_text())
    validation_errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if validation_errors:
        errors.extend(f"{vector['id']}: schema: {e.message}" for e in validation_errors)
        continue
    if data["reconstruction_status"] != vector["expected_reconstruction_status"]:
        errors.append(f"{vector['id']}: reconstruction status mismatch")
    if data["historical_effect"] != vector["expected_historical_effect"]:
        errors.append(f"{vector['id']}: historical effect mismatch")
    if data["requested_time"] < data["evaluation_time"] and data["state_at_requested_time"] == data["current_state"] and vector["id"] == "HV-12-current-state-not-substituted":
        errors.append("HV-12: current state substituted for historical state")
    if data["evidence"]["integrity_status"] == "failed" and data["reconstruction_status"] not in ("indeterminate", "reconstructed_partial", "authoritative_partial"):
        errors.append(f"{vector['id']}: integrity failure yielded unqualified historical result")
    if data["retention"]["status"] == "outside_retention" and data["reconstruction_status"] != "indeterminate":
        errors.append(f"{vector['id']}: retention boundary must be indeterminate")
    results.append({"id": vector["id"], "passed": True, "reconstruction_status": data["reconstruction_status"], "historical_effect": data["historical_effect"]})

if errors:
    print("\n".join(errors))
    sys.exit(1)

ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
evidence = {"profile": manifest["profile"], "version": manifest["version"], "passed": True, "vector_count": len(results), "results": results}
(ARTIFACT_DIR / "evidence-bundle.json").write_text(json.dumps(evidence, indent=2) + "\n")
print(f"validate_historical_resolution.py: {len(results)}/{len(manifest['vectors'])} historical vectors passed")
