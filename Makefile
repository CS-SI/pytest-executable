# Copyright 2020 CS Systemes d'Information, http://www.c-s.fr
#
# This file is part of pytest-executable
#     https://www.github.com/CS-SI/pytest-executable
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
SHELL=/bin/bash

NAME=pytest_executable
ENV_NAME=pytest_executable

CONDA_ACTIVATE=set -e; \
	       source $$(conda info --base)/etc/profile.d/conda.sh; \
	       conda activate $(ENV_NAME)

# configure conda
config:
	conda config --add channels conda-forge
	conda config --set channel_priority strict

# create the anaconda environment
create: config
	conda create --yes --name $(ENV_NAME) python=3.7 pip

# install the development requirements
requirements-dev:
	$(CONDA_ACTIVATE); \
	pip install --requirement requirements-dev.txt

# prepare the anaconda environment with the dev requirements
environment: create requirements-dev

# all the following targets shall be executed after having activated an environment

# install the requirements
requirements:
	conda install --yes $$(cat requirements.txt)

# install for development
develop: requirements
	pip install --force-reinstall --no-deps --editable .

install: requirements
	pip install --force-reinstall --no-deps .

.PHONY: doc
doc:
	cd doc && make html

# directory where the files used by the ci are placed
ci-dir:
	rm -rf .ci
	mkdir -p .ci

test: ci-dir
	LC_ALL=C \
	pytest -v \
		--cov $(NAME) \
		--cov-report html \
		--cov-config setup.cfg \
		tests

# TODO: mypy --txt-report .ci/mypy.log $(NAME) tests
mypy: ci-dir
	mypy $(NAME) tests

pylint: ci-dir
	pylint -f parseable $(NAME) tests | tee .ci/pylint.log

flake8: ci-dir
	flake8 --tee --output-file .ci/flake8.log $(NAME) tests

check: mypy flake8

black:
	black -t py37 --exclude _version.py tests $(NAME)

isort:
	isort --recursive --apply tests $(NAME)

style: isort black
