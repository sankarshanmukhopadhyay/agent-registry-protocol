.PHONY: pilot-up pilot-down pilot-seed pilot-check pilot-reset  setup validate test interop candidate run report pages-manifest pages-build pages-validate pages-check release-check package clean
setup:
	python3 -m pip install -r scripts/requirements.txt
validate:
	python3 scripts/validate_examples.py
	python3 scripts/validate_test_vectors.py
	python3 scripts/validate_extended_vectors.py
	python3 scripts/validate_artifacts.py
	python3 scripts/validate_repository.py
	python3 scripts/validate_candidate.py
test:
	python3 -m pytest -q
interop:
	python3 scripts/run_interoperability.py
candidate:
	python3 scripts/run_candidate_program.py
run:
	python3 -m uvicorn reference.app:app --host 127.0.0.1 --port 8000
report:
	python3 scripts/generate_implementation_report.py

pages-manifest:
	python3 scripts/build_publication_manifest.py
pages-build:
	bundle exec jekyll build --trace --baseurl "/agent-registry-protocol"
pages-validate:
	python3 scripts/validate_publication.py --baseurl "/agent-registry-protocol"
pages-check: pages-manifest pages-build pages-validate
release-check: validate test interop candidate report
package: release-check
clean:
	rm -rf .pytest_cache __pycache__ reference/__pycache__ scripts/__pycache__ independent_impl/__pycache__


pilot-up:
	docker compose up --build -d

pilot-down:
	docker compose down

pilot-reset:
	docker compose down -v

pilot-seed:
	python3 implementation-accelerator/scripts/seed_registry.py

pilot-check:
	python3 scripts/validate_pilot.py
