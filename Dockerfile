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
FROM continuumio/miniconda3

ENV name=pytest_executable \
    env_name=pytest_executable

# preparation for other steps
# write the conda configuration globally for all users
RUN apt-get update \
    && apt-get install -y make gcc \
    && conda update -n base -c defaults conda \
    && conda install conda-build -y \
    && conda config --add channels conda-forge  --file /opt/conda/.condarc \
    && conda config --set channel_priority strict --file /opt/conda/.condarc

# create the anaconda environment
COPY Makefile \
     requirements-dev.txt \
     ./
RUN make environment \
    && conda clean -tipy

# install requirements
COPY setup.* \
     versioneer.py \
     requirements.txt \
     ./
RUN . /opt/conda/etc/profile.d/conda.sh \
    && conda activate $env_name \
    && make requirements \
    && conda clean -tipy

# allow all users to create anaconda pkgs and envs
RUN chmod og+w -R /opt/conda
