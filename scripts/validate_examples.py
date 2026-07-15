#!/usr/bin/env python3
"""
validate_examples.py

Validates every file under examples/valid/ and examples/invalid/ against the
corresponding record-family JSON Schema in schemas/.

Mapping rule: examples/{valid,invalid}/<name>.json is validated against
schemas/<name>.schema.json.

Expected outcome:
  - examples/valid/*.json    MUST validate with zero schema errors.
  - examples/invalid/*.json  MUST fail validation (at least one schema error).
    Each invalid example carries a "_violation" field (ignored by the schema,
    since additionalProperties is not restricted) documenting which
    normative requirement it breaks, for human review.

Run from the repository root:

    python3 scripts/validate_examples.py

Exit code is 0 only if every example produced the expected outcome. Prints a
final "PASS_COUNT/TOTAL_COUNT OK" line suitable for pasting into a commit
message, per this repository's contribution and hygiene requirements.

Dependencies: jsonschema>=4.18, referencing (installed transitively with
jsonschema>=4.18). See scripts/requirements.txt.
"""

from __future__ import annotations

import json
import pathlib
import sys

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError as exc:  # pragma: no cover
    sys.stderr.write(
        "Missing dependency: {}\n"
        "Install with: pip install -r scripts/requirements.txt "
        "(add --break-system-packages on externally-managed Python installs)\n".format(exc)
    )
    sys.exit(2)

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMAS_DIR = REPO_ROOT / "schemas"
EXAMPLES_DIR = REPO_ROOT / "examples"


def build_registry() -> Registry:
    resources = []
    for path in SCHEMAS_DIR.rglob("*.schema.json"):
        doc = json.loads(path.read_text())
        resources.append(Resource.from_contents(doc))
    return Registry().with_resources((r.id(), r) for r in resources if r.id())


def load_schema(name: str) -> dict:
    schema_path = SCHEMAS_DIR / f"{name}.schema.json"
    if not schema_path.exists():
        raise FileNotFoundError(
            f"No schema {schema_path.relative_to(REPO_ROOT)} for example set '{name}'. "
            "Every example file must have a matching schemas/<name>.schema.json."
        )
    return json.loads(schema_path.read_text())


def validate_one(name: str, instance_path: pathlib.Path, registry: Registry) -> list[str]:
    schema = load_schema(name)
    validator = Draft202012Validator(schema, registry=registry)
    instance = json.loads(instance_path.read_text())
    return [
        f"{err.json_path}: {err.message}"
        for err in sorted(validator.iter_errors(instance), key=lambda e: e.json_path)
    ]


def main() -> int:
    registry = build_registry()

    results = []  # (label, path, expected_valid, errors)

    valid_dir = EXAMPLES_DIR / "valid"
    invalid_dir = EXAMPLES_DIR / "invalid"

    for path in sorted(valid_dir.glob("*.json")):
        name = path.stem
        errors = validate_one(name, path, registry)
        results.append(("valid", path, True, errors))

    for path in sorted(invalid_dir.glob("*.json")):
        name = path.stem
        errors = validate_one(name, path, registry)
        results.append(("invalid", path, False, errors))

    total = len(results)
    passed = 0
    failures = []

    for label, path, expected_valid, errors in results:
        is_valid = len(errors) == 0
        ok = is_valid == expected_valid
        rel = path.relative_to(REPO_ROOT)
        if ok:
            passed += 1
            status = "OK"
        else:
            status = "UNEXPECTED"
            failures.append((rel, label, expected_valid, errors))
        if label == "valid":
            print(f"[{status}] {rel}: expected valid, got {'valid' if is_valid else 'INVALID'}")
        else:
            print(f"[{status}] {rel}: expected invalid, got {'invalid' if not is_valid else 'VALID'}")
        if errors and (label == "invalid"):
            for e in errors:
                print(f"    - {e}")
        if errors and label == "valid":
            for e in errors:
                print(f"    ! {e}")

    print()
    print(f"validate_examples.py: {passed}/{total} OK")

    if failures:
        print()
        print("FAILURES:")
        for rel, label, expected_valid, errors in failures:
            print(f"  {rel} (expected {'valid' if expected_valid else 'invalid'} example set '{label}')")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
