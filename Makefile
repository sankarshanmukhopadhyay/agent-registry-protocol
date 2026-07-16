.PHONY: setup validate test interop run report release-check package clean
setup:
	python3 -m pip install -r scripts/requirements.txt
validate:
	python3 scripts/validate_examples.py
	python3 scripts/validate_test_vectors.py
	python3 scripts/validate_extended_vectors.py
	python3 scripts/validate_artifacts.py
	python3 scripts/validate_repository.py
test:
	python3 -m pytest -q
interop:
	python3 scripts/run_interoperability.py
run:
	python3 -m uvicorn reference.app:app --host 127.0.0.1 --port 8000
report:
	python3 scripts/generate_implementation_report.py
release-check: validate test interop report
package: release-check
clean:
	rm -rf artifacts .pytest_cache __pycache__ reference/__pycache__ scripts/__pycache__
