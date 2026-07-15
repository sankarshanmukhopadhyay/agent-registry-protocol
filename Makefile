.PHONY: setup validate test run report package
setup:
	python3 -m pip install -r scripts/requirements.txt
validate:
	python3 scripts/validate_examples.py
	python3 scripts/validate_test_vectors.py
	python3 scripts/validate_extended_vectors.py
	python3 scripts/validate_artifacts.py
test:
	python3 -m pytest -q
run:
	python3 -m uvicorn reference.app:app --host 127.0.0.1 --port 8000
report:
	python3 scripts/generate_implementation_report.py
package:
	python3 scripts/generate_implementation_report.py
