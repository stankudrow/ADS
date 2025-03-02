SRC := adspy

.PHONY: check format lint test

check:
	ruff format --check
	ruff check
	mypy ${SRC}

format:
	ruff format

lint: format
	ruff check --fix .

test:
	pytest tests
