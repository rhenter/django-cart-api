VERSION=$(shell cat CHANGES.rst | head -n 1 | awk '{print $1}')

clean: clean-eggs clean-build
	@find . -iname '*.pyc' -exec rm -rf {} \;
	@find . -iname '*.pyo' -exec rm -rf {} \;
	@find . -iname '*~' -exec rm -rf {} \;
	@find . -iname '*.swp' -exec rm -rf {} \;
	@find . -iname '__pycache__' -exec rm -rf {} \;
	@find . -name ".pytest_cache"  -exec rm -rf {} \;
	@find . -name ".cache"  -exec rm -rf {} \;


clean-eggs:
	@find . -name '*.egg' -print0|xargs -0 rm -rf --
	@rm -rf .eggs/

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

deps:
	pip install -r requirements/test.txt

autopep8:
	autopep8 --in-place -a -a -a -a -j 3 -v -r ./src

test: deps
	py.test -vvv

${VIRTUAL_ENV}/bin/pip-sync:
	pip install pip-tools

run:
	python src/manage.py runserver

migrations:
	python src/manage.py makemigrations

migrate:
	python src/manage.py migrate

pip-tools: ${VIRTUAL_ENV}/bin/pip-sync

pip-compile: pip-tools
	pip-compile requirements/production.in -vvv

pip-install: pip-compile
	pip install --upgrade -r requirements/local.txt

pip-upgrade: pip-tools
	pip-compile --upgrade requirements/production.in -vvv

view-version:
	@echo "${VERSION}";