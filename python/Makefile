.PHONY: check format lint test

check:
	ruff format --check
	ruff check
	mypy

format:
	ruff format

lint: format
	ruff check --fix .

test:
	pytest
