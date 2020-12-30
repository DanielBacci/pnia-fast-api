clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

install:
	@pip install -r requirements/production.txt

install-dev:
	@pip install -r requirements/development.txt

run:
	@uvicorn source.routes:app --reload --port "8000"

lint:
	@flake8
	@isort "source" --check

lint-fix:
	@isort "source" --interactive

detect-outdated-dependencies:
	@sh -c 'output=$$(pip list --outdated); echo "$$output"; test -z "$$output"'

test: clean
	@py.test
