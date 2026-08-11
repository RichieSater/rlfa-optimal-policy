.PHONY: install test lint check certificate search benchmark paper clean

install:
	uv sync --extra test

test:
	uv run pytest
	uv run python -m rlfa_optimal_policy verify
	uv run python -m rlfa_optimal_policy verify-industry
	uv run python scripts/independent_verify.py
	uv run python scripts/independent_verify_industry.py

lint:
	uv run ruff check .

check: lint test

certificate:
	uv run python -m rlfa_optimal_policy certificate --output certificates/counterexample.json
	uv run python -m rlfa_optimal_policy verify
	uv run python -m rlfa_optimal_policy industry-certificate --output certificates/industry-results.json
	uv run python -m rlfa_optimal_policy verify-industry

search:
	uv run python -m rlfa_optimal_policy search-n2 --max-denominator 6

benchmark:
	uv run python scripts/generate_small_benchmarks.py
	uv run python scripts/benchmark_certified_scores.py

paper:
	tectonic --keep-logs --keep-intermediates paper/main.tex

clean:
	find paper -maxdepth 1 -type f \( -name '*.aux' -o -name '*.log' -o -name '*.out' -o -name '*.toc' \) -delete
