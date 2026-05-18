PY ?= python
PIP ?= pip

.PHONY: install test mutate gui ci clean hooks

install:
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

hooks:
	git config core.hooksPath .githooks || true

test:
	PYTHONPATH=src $(PY) -m pytest -q

mutate:
	PYTHONPATH=src $(PY) -m mutmut run || true
	PYTHONPATH=src $(PY) -m mutmut results

gui:
	PYTHONPATH=src $(PY) -m roman.gui

ci: test mutate

clean:
	rm -rf .mutmut-cache .pytest_cache **/__pycache__ build dist *.egg-info
