.PHONY: check format lint test

check:
	ruff format --check
	ruff check

format:
	ruff format

lint: format
	ruff check --fix .

test:
	pytest tests
