.DEFAULT_GOAL := help

ifeq ($(OS),Windows_NT)
	export DELETE_DIST=del /f /q dist\\*
	export MYPYPATH=dcr_core
	export PYTHON=python
	export PYTHONPATH=dcr_core
else
	export DELETE_DIST=rm -f dist/*
	export MYPYPATH=dcr_core
	export PYTHON=python3
	export PYTHONPATH=dcr_core
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
## dev:                Format and lint the code.
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
	pipenv run black ${PYTHONPATH}
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
	pipenv run docformatter --in-place -r ${PYTHONPATH}
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
	pipenv run flake8 ${PYTHONPATH}
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
	pipenv run isort ${PYTHONPATH}
	@echo Info **********  End:   isort ***************************************

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
	pipenv run mypy ${PYTHONPATH}
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
	pipenv run pip freeze
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
	pipenv run pip freeze
	${PYTHON} --version
	${PYTHON} -m pip --version
	@echo Info **********  End:   Installation of Production Packages *********

# Pydoc-Markdown - create Python API documentation in Markdown format.
# https://github.com/NiklasRosenstein/pydoc-markdown
# Configuration file: pyproject.toml
pydoc-markdown:     ## Create Python API documentation in Markdown format with Pydoc-Markdown.
	@echo Info **********  Start: Pydoc-Markdown ******************************
	@echo MYPYPATH  =${MYPYPATH}
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	pipenv run pydoc-markdown --version
	@echo ---------------------------------------------------------------------
	pipenv run pydoc-markdown -I ${PYTHONPATH} --render-toc > docs/developing_api_documentation.md
	@echo Info **********  End:   Pydoc-Markdown ******************************

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
	pipenv run pydocstyle --count ${PYTHONPATH}
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
	pipenv run pylint ${PYTHONPATH}
	@echo Info **********  End:   Pylint **************************************

# twine: Collection of utilities for publishing packages on bPyPI.
# https://pypi.org/project/twine/
upload:             ## Upload the distribution archive to PyPi.
	@echo Info **********  Start: twine prod **********************************
	@echo MYPYPATH  =${MYPYPATH}
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	${PYTHON} -m build --version
	${PYTHON} -m twine --version
	@echo ---------------------------------------------------------------------
	${PYTHON} -m build
	${PYTHON} -m twine upload -p $(SECRET_PYPI) -u wwe dist/*
	@echo Info **********  End:   twine prod ***********************************

# twine: Collection of utilities for publishing packages on Test bPyPI.
# https://pypi.org/project/twine/
# https://test.pypi.org
upload-test:        ## Upload the distribution archive to Test PyPi.
	@echo Info **********  Start: twine test **********************************
	@echo DELETE_DIST=${DELETE_DIST}
	@echo MYPYPATH   =${MYPYPATH}
	@echo PYTHON     =${PYTHON}
	@echo PYTHONPATH =${PYTHONPATH}
	${PYTHON} -m build --version
	${PYTHON} -m twine --version
	@echo ---------------------------------------------------------------------
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
