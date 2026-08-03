PY ?= python3
PIP ?= pip

.PHONY: install test cov run clean

install:
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

test:
	$(PY) -m pytest -q

cov:
	$(PY) -m pytest --cov=roman.converter --cov-branch --cov-report=term-missing

run:
	$(PY) -m roman

clean:
	rm -rf .pytest_cache **/__pycache__ build dist *.egg-info .coverage
