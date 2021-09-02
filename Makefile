.PHONY: all build install typing lint test docs

all: black build install typing lint test docs

black:
	black -l 99 here_location_services tests docs/notebooks
	isort --atomic .

build:
	python3 -m pip install -r requirements.txt

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

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
	rm -fr .mypy_cache
	rm -fr .pytest_cache
	find . -name '.ipynb_checkpoints' -exec rm -fr {} +
	rm -fr docs/source/_build

install:
	python3 -m pip install -e .

typing:
	pytest -v -s --mypy here_location_services

lint:
	isort --check --diff here_location_services tests
	flake8 -v --statistics --count .
	black -l 99 --diff --check here_location_services tests docs/notebooks

test:
	pytest -v -s --cov=here_location_services tests
	coverage html

docs:
	sh scripts/build_docs.sh
