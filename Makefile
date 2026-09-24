.PHONY: dev

KB ?= ../shopsystem-kb

dev:
	pip install -e $(KB) -e '.[dev]'
