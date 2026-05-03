.PHONY: all install autoupdate lint clean test unit-tests e2e-tests

all: install lint test

install:
	pre-commit install

autoupdate:
	pre-commit autoupdate

lint:
	pre-commit run --all-files

clean:
	pre-commit clean

unit-tests:
	uv run pytest -vv --cov=pyfilesmanager --cov-fail-under=100 tests/unit/

e2e-tests:
	uv run pytest -vv tests/e2e/

test: unit-tests e2e-tests
