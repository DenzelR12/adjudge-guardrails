.PHONY: install test freshness verify

install:
	python -m pip install -e ".[dev]"

test:
	python -m pytest -q

freshness:
	python -m adjudge.cli freshness --registry configs/metrics.example.json

verify:
	python -m adjudge.cli verify --registry configs/metrics.example.json
