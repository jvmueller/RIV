.PHONY: bootstrap run

PYTHON ?= python
MODULE ?= web.app


run:
	$(PYTHON) -m $(MODULE)



bootstrap:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && $(PIP) install -r requirements.txt