.PHONY: dev dev-local test

# One virtualenv per checkout. shop-knowledge installs the kb tag its pyproject pins.
dev:
	python3 -m venv .venv
	.venv/bin/pip install -e '.[dev]'

# For work that needs an unreleased kb: install the sibling checkout editable instead of the pin.
# Anything that only works this way is a request to bump the pin, not a state to ship from.
KB ?= ../shopsystem-kb
dev-local: dev
	.venv/bin/pip install -e $(KB)

test:
	.venv/bin/python -m pytest -q
