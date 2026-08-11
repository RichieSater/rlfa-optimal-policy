.PHONY: install test lint check certificate search paper clean

install:
	uv sync --extra test

test:
	uv run pytest
	uv run python -m rlfa_optimal_policy verify
	uv run python scripts/independent_verify.py

lint:
	uv run ruff check .

check: lint test

certificate:
	uv run python -m rlfa_optimal_policy certificate --output certificates/counterexample.json
	uv run python -m rlfa_optimal_policy verify

search:
	uv run python -m rlfa_optimal_policy search-n2 --max-denominator 6

paper:
	tectonic --keep-logs --keep-intermediates paper/main.tex

clean:
	find paper -maxdepth 1 -type f \( -name '*.aux' -o -name '*.log' -o -name '*.out' -o -name '*.toc' \) -delete
