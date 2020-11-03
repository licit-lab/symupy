
.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help



define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT



define BROWSER_PYSCRIPT

import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef

export BROWSER_PYSCRIPT



define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef

export PRINT_HELP_PYSCRIPT



BROWSER := python -c "$$BROWSER_PYSCRIPT"


clean: clean-build clean-pyc clean-test clean-doc ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -fr .ipynb_checkpoints

clean-doc: ## remove automatic doc generation
	rm -fr docs/source/symupy*


help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

lint: ## check style with black
	black --line-length 120 symupy

test: ## run tests quickly with the default Python
	pytest

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/source/symupy.rst
	rm -f docs/source/modules.rst
	rm -f docs/source/symupy.*.rst	
	sphinx-apidoc -o docs/source symupy
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/build/html/index.html

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
	twine check dist/*

develop: clean ## install developer mode
	pip install --editable .

install: clean ## install the package to the active Python's site-packages
	python setup.py install
