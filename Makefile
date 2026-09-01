.PHONY: install test freshness verify report

install:
	python -m pip install -e ".[dev]"

test:
	python -m pytest -q

freshness:
	python -m adjudge.cli freshness --registry configs/metrics.example.json

verify:
	python -m adjudge.cli verify --registry configs/metrics.example.json

report:
	python -m adjudge.cli report --registry configs/metrics.example.json --waivers configs/waivers.example.json
