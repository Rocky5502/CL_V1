.PHONY: setup preflight test lint pilot benchmark tier-a tier-b analyze paper-artifacts
setup:
	bash scripts/setup_wsl.sh
preflight:
	python scripts/preflight.py --write artifacts/preflight
lint:
	ruff check src scripts tests

test:
	pytest -q
pilot:
	python scripts/build_benchmark.py --pilot
	python scripts/run_pilot.py --model mock
benchmark:
	python scripts/build_benchmark.py --target configs/experiment.yaml

tier-a:
	python scripts/run_experiment.py --tier A --config configs/experiment.yaml

tier-b:
	python scripts/run_experiment.py --tier B --config configs/experiment.yaml
analyze:
	python scripts/analyze_results.py --config configs/experiment.yaml
paper-artifacts:
	python scripts/make_paper_artifacts.py --config configs/experiment.yaml
