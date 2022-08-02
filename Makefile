.DEFAULT_GOAL := help

ifeq ($(OS),Windows_NT)
	DCR_DOCKER_CONTAINER=scripts\\run_setup_postgresql.bat test
	export PYTHON=python
	export MYPYPATH=src\\dcr_core
	export PYTHONPATH=src\\dcr_core
else
	DCR_DOCKER_CONTAINER=./scripts/run_setup_postgresql.sh test
	export PYTHON=python3
	export MYPYPATH=src/dcr_core
	export PYTHONPATH=src/dcr_core
endif

##                                                                            .
## ============================================================================
## DCR - Document Content Recognition - make Documentation.
##       ---------------------------------------------------------------
##       The purpose of this Makefile is to support the whole software
##       development process for DCR. it contains also the necessary
##       tools for the CI activities.
##       ---------------------------------------------------------------
##       The available make commands are:
## ----------------------------------------------------------------------------
## help:               Show this help.
## ----------------------------------------------------------------------------
## dev:                Format and lintthe code.
dev: format lint pydocstyle
## docs:               Check the API docs, create and upload the user docs.
# docs: pydocstyle pydoc-markdown mkdocs
docs: pydocstyle mkdocs
## format:             Format the code with isort, Black and docformatter.
format: isort black docformatter
## lint:               Lint the code with Bandit, Flake8, Pylint and Mypy.
lint: bandit flake8 pylint mypy
## ----------------------------------------------------------------------------

help:
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

# Bandit is a tool designed to find common security issues in Python code.
# https://github.com/PyCQA/bandit
# Configuration file: none
bandit:             ## Find common security issues with Bandit.
	@echo "Info **********  Start: Bandit **************************************"
	@echo "MYPYPATH  =${MYPYPATH}"
	@echo "PYTHON    =${PYTHON}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "---------------------------------------------------------------------"
	pipenv run bandit --version
	pipenv run bandit -c pyproject.toml -r src
	@echo "Info **********  End:   Bandit **************************************"

# The Uncompromising Code Formatter
# https://github.com/psf/black
# Configuration file: pyproject.toml
black:              ## Format the code with Black.
	@echo "Info **********  Start: black ***************************************"
	@echo "MYPYPATH  =${MYPYPATH}"
	@echo "PYTHON    =${PYTHON}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "---------------------------------------------------------------------"
	pipenv run black --version
	pipenv run black src
	@echo "Info **********  End:   black ***************************************"

# Byte-compile Python libraries
# https://docs.python.org/3/library/compileall.html
# Configuration file: none
compileall:         ## Byte-compile the Python libraries.
	@echo "Info **********  Start: Compile All Python Scripts ******************"
	@echo "MYPYPATH  =${MYPYPATH}"
	@echo "PYTHON    =${PYTHON}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "---------------------------------------------------------------------"
	${PYTHON} --version
	${PYTHON} -m compileall
	@echo "Info **********  End:   Compile All Python Scripts ******************"

# Formats docstrings to follow PEP 257
# https://github.com/PyCQA/docformatter
# Configuration file: none
docformatter:       ## Format the docstrings with docformatter.
	@echo "Info **********  Start: docformatter ********************************"
	@echo "MYPYPATH  =${MYPYPATH}"
	@echo "PYTHON    =${PYTHON}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "---------------------------------------------------------------------"
	pipenv run docformatter --version
	pipenv run docformatter --in-place -r src
	@echo "Info **********  End:   docformatter ********************************"

# Flake8: Your Tool For Style Guide Enforcement.
# includes McCabe:      https://github.com/PyCQA/mccabe
# includes pycodestyle: https://github.com/PyCQA/pycodestyle
# includes Pyflakes:    https://github.com/PyCQA/pyflakes
# includes Radon:       https://github.com/rubik/radon
# https://github.com/pycqa/flake8
# Configuration file: cfg.cfg
flake8:             ## Enforce the Python Style Guides with Flake8.
	@echo "Info **********  Start: Flake8 **************************************"
	@echo "MYPYPATH  =${MYPYPATH}"
	@echo "PYTHON    =${PYTHON}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "---------------------------------------------------------------------"
	pipenv run flake8 --version
	pipenv run flake8 --exclude TET.py src
	@echo "Info **********  End:   Flake8 **************************************"

# isort your imports, so you don't have to.
# https://github.com/PyCQA/isort
# Configuration file: pyproject.toml
isort:              ## Edit and sort the imports with isort.
	@echo "Info **********  Start: isort ***************************************"
	@echo "MYPYPATH  =${MYPYPATH}"
	@echo "PYTHON    =${PYTHON}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "---------------------------------------------------------------------"
	pipenv run isort --version
	pipenv run isort src
	@echo "Info **********  End:   isort ***************************************"

# Project documentation with Markdown.
# https://github.com/mkdocs/mkdocs/
# Configuration file: none
mkdocs:             ## Create and upload the user documentation with MkDocs.
	@echo "Info **********  Start: MkDocs **************************************"
	@echo "MYPYPATH  =${MYPYPATH}"
	@echo "PYTHON    =${PYTHON}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "---------------------------------------------------------------------"
	pipenv run mkdocs --version
	pipenv run mkdocs gh-deploy --force
	@echo "Info **********  End:   MkDocs **************************************"

# Mypy: Static Typing for Python
# https://github.com/python/mypy
# Configuration file: pyproject.toml
mypy:               ## Find typing issues with Mypy.
	@echo "Info **********  Start: Mypy ****************************************"
	@echo "MYPYPATH  =${MYPYPATH}"
	@echo "PYTHON    =${PYTHON}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "---------------------------------------------------------------------"
	pipenv run pip freeze | grep mypy
	pipenv run mypy --version
	pipenv run mypy --exclude src/dcr_core/TET.py src/dcr_core
	@echo "Info **********  End:   Mypy ****************************************"

# pip is the package installer for Python.
# https://pypi.org/project/pip/
# Configuration file: none
# Pipenv: Python Development Workflow for Humans.
# https://github.com/pypa/pipenv
# Configuration file: Pipfile
pipenv-dev:         ## Install the package dependencies for development.
	@echo "Info **********  Start: Installation of Development Packages ********"
	@echo "MYPYPATH  =${MYPYPATH}"
	@echo "PYTHON    =${PYTHON}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "---------------------------------------------------------------------"
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install --upgrade pipenv
	${PYTHON} -m pipenv install --dev
	${PYTHON} -m pipenv --rm
	exit
	${PYTHON} -m pipenv update --dev
	pipenv run pip freeze
	${PYTHON} --version
	${PYTHON} -m pip --version
	@echo "Info **********  End:   Installation of Development Packages ********"
pipenv-prod:        ## Install the package dependencies for production.
	@echo "Info **********  Start: Installation of Production Packages *********"
	@echo "MYPYPATH  =${MYPYPATH}"
	@echo "PYTHON    =${PYTHON}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "---------------------------------------------------------------------"
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install --upgrade pipenv
	${PYTHON} -m pipenv install
	${PYTHON} -m pipenv --rm
	exit
	${PYTHON} -m pipenv update
	pipenv run pip freeze
	${PYTHON} --version
	${PYTHON} -m pip --version
	@echo "Info **********  End:   Installation of Production Packages *********"

# Pydoc-Markdown - create Python API documentation in Markdown format.
# https://github.com/NiklasRosenstein/pydoc-markdown
# Configuration file: pyproject.toml
pydoc-markdown:     ## Create Python API documentation in Markdown format with Pydoc-Markdown.
	@echo "Info **********  Start: Pydoc-Markdown ******************************"
	@echo "MYPYPATH  =${MYPYPATH}"
	@echo "PYTHON    =${PYTHON}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "---------------------------------------------------------------------"
	pipenv run pydoc-markdown --version
	pipenv run pydoc-markdown -I src/dcr_core --render-toc > docs/developing_api_documentation.md
	@echo "Info **********  End:   Pydoc-Markdown ******************************"

# pydocstyle - docstring style checker.
# https://github.com/PyCQA/pydocstyle
# Configuration file: pyproject.toml
pydocstyle:         ## Check the API documentation with pydocstyle.
	@echo "Info **********  Start: pydocstyle **********************************"
	@echo "MYPYPATH  =${MYPYPATH}"
	@echo "PYTHON    =${PYTHON}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "---------------------------------------------------------------------"
	pipenv run pydocstyle --version
	pipenv run pydocstyle --count src
	@echo "Info **********  End:   pydocstyle **********************************"

# Pylint is a tool that checks for errors in Python code.
# https://github.com/PyCQA/pylint/
# Configuration file: .pylintrc
pylint:             ## Lint the code with Pylint.
	@echo "Info **********  Start: Pylint **************************************"
	@echo "MYPYPATH  =${MYPYPATH}"
	@echo "PYTHON    =${PYTHON}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "---------------------------------------------------------------------"
	pipenv run pylint --version
	pipenv run pylint src
	@echo "Info **********  End:   Pylint **************************************"

## ============================================================================
