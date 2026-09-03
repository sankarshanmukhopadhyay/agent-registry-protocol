# Validation commands

The KYA-OS → ARPA profile participates in the repository-wide validation gate through `make validate`.

Focused checks:

```bash
python3 scripts/validate_kya_os_profile.py
pytest -q tests/test_validate_kya_os_profile.py
```

A profile pass means the machine-readable corpus is schema-valid and that expected outcomes preserve the ARPA-side authority boundary encoded by the reference adapter. It does not verify KYA-OS cryptography or claim live interoperability.
