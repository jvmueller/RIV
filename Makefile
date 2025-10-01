.PHONY: bootstrap run

PYTHON := $(shell which python3 || which python)
MODULE ?= web.app
CLI ?= demand.main


run:
	$(PYTHON) -m $(MODULE)


cli:
	$(PYTHON) -m $(CLI)


bootstrap:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && $(PIP) install -r requirements.txt