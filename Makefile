.PHONY: help venv test app docker

APPDIR = app
APPNAME = `cat ${APPDIR}/name`
VERSION =`cat ${APPDIR}/version`
VENV = venv/bin

_COL_PINK_BOLD = \033[1m\033[35m
_COL_GREEN_BOLD = \033[1m\033[32m 
_COL_OFF = \033[0m

help:
	@echo
	@echo "${_COL_PINK_BOLD} ${APPNAME} ${VERSION}${NORMAL}" 
	@echo
	@echo "${_COL_GREEN_BOLD}Please use 'make ${_COL_GREEN_BOLD}target${_COL_OFF}' where ${_COL_GREEN_BOLD}target${_COL_OFF} is one of:"
	@echo
	@echo "${_COL_GREEN_BOLD}   venv              ${_COL_OFF} to create a virtual environment"
	@echo "${_COL_GREEN_BOLD}   venv-dev          ${_COL_OFF} to create a developer virtual environment"
	@echo "${_COL_GREEN_BOLD}   clean             ${_COL_OFF} to clean clean all automatically generated files"
	@echo "${_COL_GREEN_BOLD}   run               ${_COL_OFF} to run app"
	@echo "${_COL_GREEN_BOLD}   format            ${_COL_OFF} to format code with 'black' formatter"
	@echo "${_COL_GREEN_BOLD}   pylint            ${_COL_OFF} to checks for errors in Python code"
	@echo "${_COL_GREEN_BOLD}   docker-build      ${_COL_OFF} to build docker image"
	@echo
	
clean:
	@find . -name \*.pyc -delete
	@find . -name \*log -exec rm -r {} +
	@find . -name \*__pycache__ -delete
	@find . -name \*venv -exec rm -r {} +
	@find . -name \*.pytest_cache -exec rm -r {} +
	@find . -name \*.log -exec rm -r {} +

venv:
	@python3 -m venv venv
	@${VENV}/pip3 install -U -r requirements.txt

venv-dev:
	@python3 -m venv venv
	@${VENV}/pip3 install -U -r requirements.txt
	@${VENV}/pip3 install -U -r requirements-dev.txt

run:
	@export ENV_FOR_DYNACONF=default; ${PWD}/${VENV}/python3  ${PWD}/${APPDIR}/main.py
	
format:
	@${VENV}/black ${APPDIR}

pylint:
	@${VENV}/pylint ${APPDIR}

docker-build:
	@docker build -t ${APPNAME}:develop -f docker/Dockerfile .
