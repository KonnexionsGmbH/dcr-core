.DEFAULT_GOAL := help

ifeq ($(OS),Windows_NT)
	export CREATE_DIST=if not exist dist mkdir dist
	export CREATE_DOCS=if not exist docs\\api-docs mkdir docs\\api-docs
	export DELETE_DIST=del /f /q dist\\*
	export DELETE_DOCS=del /f /q docs\\api-docs\\*
	export MYPYPATH=
	export PYTHON=python
	export PYTHONPATH=dcr_core
else
	export CREATE_DIST=mkdir -p dist
	export CREATE_DOCS=mkdir -p docs/api-docs
	export DELETE_DIST=rm -f dist/*
	export DELETE_DOCS=rm -f docs/api-docs/*
	export MYPYPATH=
	export PYTHON=python3
	export PYTHONPATH=dcr_core
endif

##                                                                            .
## ============================================================================
## DCR-CORE - Document Content Recognition API - make Documentation.
##            ---------------------------------------------------------------
##            The purpose of this Makefile is to support the whole software
##            development process for DCR-CORE. it contains also the necessary
##            tools for the CI activities.
##            ---------------------------------------------------------------
##            The available make commands are:
## ----------------------------------------------------------------------------
## help:               Show this help.
## ----------------------------------------------------------------------------
## dev:                Format, lint and test the code.
dev: format lint tests
## docs:               Check the API documentation, create and upload the user documentation.
docs: pydocstyle lazydocs mkdocs
## final:              Format, lint and test the code and create the documentation.
final: format lint docs tests
## format:             Format the code with isort, Black and docformatter.
format: isort black docformatter
## lint:               Lint the code with Bandit, Flake8, Pylint and Mypy.
lint: bandit flake8 pylint mypy
## tests:              Run all tests with pytest.
tests: pytest
## ----------------------------------------------------------------------------

help:
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

export DCR_ENVIRONMENT_TYPE=test

# Bandit is a tool designed to find common security issues in Python code.
# https://github.com/PyCQA/bandit
# Configuration file: none
bandit:             ## Find common security issues with Bandit.
	@echo Info **********  Start: Bandit **************************************
	@echo MYPYPATH  =${MYPYPATH}
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	pipenv run bandit --version
	@echo ---------------------------------------------------------------------
	pipenv run bandit -c pyproject.toml -r ${PYTHONPATH}
	@echo Info **********  End:   Bandit **************************************

# The Uncompromising Code Formatter
# https://github.com/psf/black
# Configuration file: pyproject.toml
black:              ## Format the code with Black.
	@echo Info **********  Start: black ***************************************
	@echo MYPYPATH  =${MYPYPATH}
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	pipenv run black --version
	@echo ---------------------------------------------------------------------
	pipenv run black ${PYTHONPATH} tests
	@echo Info **********  End:   black ***************************************

# Byte-compile Python libraries
# https://docs.python.org/3/library/compileall.html
# Configuration file: none
compileall:         ## Byte-compile the Python libraries.
	@echo Info **********  Start: Compile All Python Scripts ******************
	@echo MYPYPATH  =${MYPYPATH}
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	${PYTHON} --version
	@echo ---------------------------------------------------------------------
	${PYTHON} -m compileall
	@echo Info **********  End:   Compile All Python Scripts ******************

# Python interface to coveralls.io API
# https://github.com/TheKevJames/coveralls-python
# Configuration file: none
coveralls:          ## Run all the tests and upload the coverage data to coveralls.
	@echo Info **********  Start: coveralls ***********************************
	pipenv run pytest --cov=${PYTHONPATH} --cov-report=xml tests
	@echo ---------------------------------------------------------------------
	pipenv run coveralls --service=github
	@echo Info **********  End:   coveralls ***********************************

# Formats docstrings to follow PEP 257
# https://github.com/PyCQA/docformatter
# Configuration file: none
docformatter:       ## Format the docstrings with docformatter.
	@echo Info **********  Start: docformatter ********************************
	@echo MYPYPATH  =${MYPYPATH}
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	pipenv run docformatter --version
	@echo ---------------------------------------------------------------------
	pipenv run docformatter --in-place -r ${PYTHONPATH} tests
	@echo Info **********  End:   docformatter ********************************

# Flake8: Your Tool For Style Guide Enforcement.
# includes McCabe:      https://github.com/PyCQA/mccabe
# includes pycodestyle: https://github.com/PyCQA/pycodestyle
# includes Pyflakes:    https://github.com/PyCQA/pyflakes
# includes Radon:       https://github.com/rubik/radon
# https://github.com/pycqa/flake8
# Configuration file: cfg.cfg
flake8:             ## Enforce the Python Style Guides with Flake8.
	@echo Info **********  Start: Flake8 **************************************
	@echo MYPYPATH  =${MYPYPATH}
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	pipenv run flake8 --version
	@echo ---------------------------------------------------------------------
	pipenv run flake8 --exclude TET.py ${PYTHONPATH} tests
	@echo Info **********  End:   Flake8 **************************************

# isort your imports, so you don't have to.
# https://github.com/PyCQA/isort
# Configuration file: pyproject.toml
isort:              ## Edit and sort the imports with isort.
	@echo Info **********  Start: isort ***************************************
	@echo MYPYPATH  =${MYPYPATH}
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	pipenv run isort --version
	@echo ---------------------------------------------------------------------
	pipenv run isort ${PYTHONPATH} tests
	@echo Info **********  End:   isort ***************************************

# Generate markdown API documentation for Google-style Python docstring.
# https://github.com/ml-tooling/lazydocs
# Configuration file: n/a
lazydocs:           ## Generate markdown API documentation for Google-style Python docstring.
	@echo Info **********  Start: lazydocs ************************************
	@echo CREATE_DOCS=${CREATE_DOCS}
	@echo DELETE_DOCS=${DELETE_DOCS}
	@echo MYPYPATH   =${MYPYPATH}
	@echo PYTHON     =${PYTHON}
	@echo PYTHONPATH =${PYTHONPATH}
	@echo ---------------------------------------------------------------------
	${CREATE_DOCS}
	${DELETE_DOCS}
	pipenv run lazydocs dcr_core \
						--ignored-modules tetlib_py \
						--output-path docs/api-docs \
						--overview-file README.md \
						--src-base-url https://github.com/KonnexionsGmbH/dcr-core/blob/master/ \
						--validate dcr_core
	@echo Info **********  End:   lazydocs ************************************

# Project documentation with Markdown.
# https://github.com/mkdocs/mkdocs/
# Configuration file: none
mkdocs:             ## Create and upload the user documentation with MkDocs.
	@echo Info **********  Start: MkDocs **************************************
	@echo MYPYPATH  =${MYPYPATH}
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	pipenv run mkdocs --version
	@echo ---------------------------------------------------------------------
	pipenv run mkdocs gh-deploy --force
	@echo Info **********  End:   MkDocs **************************************

# Mypy: Static Typing for Python
# https://github.com/python/mypy
# Configuration file: pyproject.toml
mypy:               ## Find typing issues with Mypy.
	@echo Info **********  Start: Mypy ****************************************
	@echo MYPYPATH  =${MYPYPATH}
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	pipenv run mypy --version
	@echo ---------------------------------------------------------------------
	pipenv run mypy --exclude TET.py ${PYTHONPATH}
	@echo Info **********  End:   Mypy ****************************************

# pip is the package installer for Python.
# https://pypi.org/project/pip/
# Configuration file: none
# Pipenv: Python Development Workflow for Humans.
# https://github.com/pypa/pipenv
# Configuration file: Pipfile
pipenv-dev:         ## Install the package dependencies for development.
	@echo Info **********  Start: Installation of Development Packages ********
	@echo MYPYPATH  =${MYPYPATH}
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ---------------------------------------------------------------------
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install --upgrade pipenv
	${PYTHON} -m pipenv install --dev
	${PYTHON} -m pipenv --rm
	exit
	${PYTHON} -m pipenv update --dev
	pipenv run spacy download en_core_web_trf
	@echo ---------------------------------------------------------------------
	pipenv run pip freeze
	@echo ---------------------------------------------------------------------
	${PYTHON} --version
	${PYTHON} -m pip --version
	@echo Info **********  End:   Installation of Development Packages ********
pipenv-prod:        ## Install the package dependencies for production.
	@echo Info **********  Start: Installation of Production Packages *********
	@echo MYPYPATH  =${MYPYPATH}
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ---------------------------------------------------------------------
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install --upgrade pipenv
	${PYTHON} -m pipenv install
	${PYTHON} -m pipenv --rm
	exit
	${PYTHON} -m pipenv update
	pipenv run spacy download en_core_web_trf
	@echo ---------------------------------------------------------------------
	pipenv run pip freeze
	@echo ---------------------------------------------------------------------
	${PYTHON} --version
	${PYTHON} -m pip --version
	@echo Info **********  End:   Installation of Production Packages *********

# pydocstyle - docstring style checker.
# https://github.com/PyCQA/pydocstyle
# Configuration file: pyproject.toml
pydocstyle:         ## Check the API documentation with pydocstyle.
	@echo Info **********  Start: pydocstyle **********************************
	@echo MYPYPATH  =${MYPYPATH}
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	pipenv run pydocstyle --version
	@echo ---------------------------------------------------------------------
	pipenv run pydocstyle --count ${PYTHONPATH} tests
	@echo Info **********  End:   pydocstyle **********************************

# Pylint is a tool that checks for errors in Python code.
# https://github.com/PyCQA/pylint/
# Configuration file: .pylintrc
pylint:             ## Lint the code with Pylint.
	@echo Info **********  Start: Pylint **************************************
	@echo MYPYPATH  =${MYPYPATH}
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	pipenv run pylint --version
	@echo ---------------------------------------------------------------------
	pipenv run pylint ${PYTHONPATH} tests
	@echo Info **********  End:   Pylint **************************************

# pytest: helps you write better programs.
# https://github.com/pytest-dev/pytest/
# Configuration file: pyproject.toml
pytest:             ## Run all tests with pytest.
	@echo Info **********  Start: pytest **************************************
	pipenv run pytest --version
	@echo ---------------------------------------------------------------------
	pipenv run pytest --dead-fixtures tests
	pipenv run pytest --cache-clear --cov=${PYTHONPATH} --cov-report term-missing:skip-covered --random-order -v tests
	@echo Info **********  End:   pytest **************************************
pytest-ci:          ## Run all tests with pytest after test tool installation.
	@echo Info **********  Start: pytest **************************************
	pipenv install pytest
	pipenv install pytest-cov
	pipenv install pytest-deadfixtures
	pipenv install pytest-helpers-namespace
	pipenv install pytest-random-order
	pipenv install roman
	@echo ---------------------------------------------------------------------
	pipenv run pytest --version
	@echo ---------------------------------------------------------------------
	pipenv run pytest --dead-fixtures tests
	pipenv run pytest --cache-clear --cov=${PYTHONPATH} --cov-report term-missing:skip-covered --random-order -v tests
	@echo Info **********  End:   pytest **************************************
pytest-first-issue: ## Run all tests with pytest until the first issue occurs.
	@echo Info **********  Start: pytest **************************************
	@echo DCR_ENVIRONMENT_TYPE=${DCR_ENVIRONMENT_TYPE}
	pipenv run pytest --version
	@echo ---------------------------------------------------------------------
	pipenv run pytest --cache-clear --cov=${PYTHONPATH} --cov-report term-missing:skip-covered --random-order -v -x tests
	@echo Info **********  End:   pytest **************************************
pytest-issue:       ## Run only the tests with pytest which are marked with 'issue'.
	@echo Info **********  Start: pytest **************************************
	@echo DCR_ENVIRONMENT_TYPE=${DCR_ENVIRONMENT_TYPE}
	pipenv run pytest --version
	@echo ---------------------------------------------------------------------
	pipenv run pytest --cache-clear --cov=${PYTHONPATH} --cov-report term-missing:skip-covered -m issue -s --setup-show -v -x tests
	@echo Info **********  End:   pytest **************************************
pytest-module:      ## Run tests of specific module(s) with pytest - test_all & test_cfg_cls_setup & test_db_cls.
	@echo Info **********  Start: pytest **************************************
	@echo DCR_ENVIRONMENT_TYPE=${DCR_ENVIRONMENT_TYPE}
	pipenv run pytest --version
	@echo ---------------------------------------------------------------------
	pipenv run pytest --cache-clear --cov=${PYTHONPATH} --cov-report term-missing:skip-covered -v tests/test_db_cls_action.py
	@echo Info **********  End:   pytest **************************************

# twine: Collection of utilities for publishing packages on bPyPI.
# https://pypi.org/project/twine/
upload-prod:        ## Upload the distribution archive to PyPi.
	@echo Info **********  Start: twine prod **********************************
	@echo CREATE_DIST=${CREATE_DIST}
	@echo DELETE_DIST=${DELETE_DIST}
	@echo MYPYPATH  =${MYPYPATH}
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	${PYTHON} -m build --version
	${PYTHON} -m twine --version
	@echo ---------------------------------------------------------------------
	${CREATE_DIST}
	${DELETE_DIST}
	${PYTHON} -m build
	${PYTHON} -m twine upload -p $(SECRET_PYPI) -u wwe dist/*
	@echo Info **********  End:   twine prod ***********************************

# twine: Collection of utilities for publishing packages on Test bPyPI.
# https://pypi.org/project/twine/
# https://test.pypi.org
upload-test:        ## Upload the distribution archive to Test PyPi.
	@echo Info **********  Start: twine test **********************************
	@echo CREATE_DIST=${CREATE_DIST}
	@echo DELETE_DIST=${DELETE_DIST}
	@echo MYPYPATH   =${MYPYPATH}
	@echo PYTHON     =${PYTHON}
	@echo PYTHONPATH =${PYTHONPATH}
	${PYTHON} -m build --version
	${PYTHON} -m twine --version
	@echo ---------------------------------------------------------------------
	${CREATE_DIST}
	${DELETE_DIST}
	${PYTHON} -m build
	${PYTHON} -m twine upload -p $(SECRET_TEST_PYPI) -r testpypi -u wwe --verbose dist/*
	@echo Info **********  End:   twine test ***********************************

version:            ## Show the installed software versions.
	@echo Info **********  Start: pip *****************************************
	@echo MYPYPATH  =${MYPYPATH}
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	${PYTHON} -m pip --version
	${PYTHON} -m build --version
	${PYTHON} -m twine --version
	${PYTHON} -m wheel version
	@echo Info **********  End:   pip *****************************************

## ============================================================================
