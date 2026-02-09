.PHONY: install test lint clean

install:
	pip install -e .
	pip install pytest

test:
	pytest -v

lint:
	python -m py_compile logpulse/cli.py
	python -m py_compile logpulse/analyzer.py
	python -m py_compile logpulse/reporter.py
	python -m py_compile logpulse/parsers/__init__.py
	@echo "All files compile OK"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf *.egg-info build dist
