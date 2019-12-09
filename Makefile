SHELL := bash
MAKEFLAGS += --warn-undefined-variables
.SHELLFLAGS := -euo pipefail -c
SUBMAKE_OPTS := -s
ENV_FILE=.env

###############################################################################
# Configurable constants block
###############################################################################
BINARY_NAME := zg
PACKAGE_NAME := zeroguard_cli
PIPENV_CMD_RUN := pipenv run

SPHINX_SOURCE_DIR := ./docs
SPHINX_BUILD_DIR := $(SPHINX_SOURCE_DIR)/_build
SPHINX_CMD_BUILD := $(PIPENV_CMD_RUN) sphinx-build

###############################################################################
# Guest targets
###############################################################################
.PHONY: init
init:
	pip3 install pipenv --upgrade
	pipenv install --dev

.PHONY: docs
docs:
	$(SPHINX_CMD_BUILD) $(SPHINX_SOURCE_DIR) $(SPHINX_BUILD_DIR)

.PHONY: binary
binary:
	pip3 install 'PyInstaller>=3.5.0'
	pyinstaller --onefile ./zgcli/main.py -n $(BINARY_NAME)
	rm -r build/ $(BINARY_NAME).spec

.PHONY: pypi
pypi:
	pip3 install 'twine>=1.5.0'
	python3 setup.py sdist bdist_wheel
	twine upload dist/* || :
	rm -r build/ dist/ .egg $(PACKAGE_NAME).egg-info

.PHONY: test
test:
	$(PIPENV_CMD_RUN) python3 -m pytest
