SHELL=/bin/bash

.PHONY: deps_install
deps_install:
	@echo "deps_install: installing dependencies"
	pip install -e .[dev]

.PHONY: deps_outdated
deps_outdated:
	@echo "deps_outdated: listing outdated dependencies"
	pip list --outdated --format freeze

.PHONY: deps_upgrade
deps_upgrade:
	@echo "deps_upgrade: upgrading outdated dependencies"
	pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

.PHONY: format
format:
	@echo "format: checking source code format"
	black --check --diff .

.PHONY: format_fix
format_fix:
	@echo "format_fix: fixing source code format"
	black .

.PHONY: lint
lint:
	@echo "lint: linting source code"
	pylint_runner

.PHONY: precommit
precommit: format lint test

.PHONY: test
test:
	@echo "test: running unit tests"
	tox

.PHONY: test_recreate
test_recreate:
	@echo "test_recreate: recreating virtual environment: running unit tests"
	tox -r
