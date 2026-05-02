.PHONY: all install autoupdate lint clean test

all: install lint

install:
	pre-commit install

autoupdate:
	pre-commit autoupdate

lint:
	pre-commit run --all-files

clean:
	pre-commit clean

test: lint
