# Copyright 2020, CS Systemes d'Information, http://www.c-s.fr
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
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config
# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
from __future__ import annotations

from sphinx.ext import autodoc

# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
# -- Project information -----------------------------------------------------

project = "pytest-executable"
copyright = "2019, C-S"
author = "C-S"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.napoleon",
    "sphinxcontrib.spelling",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Extension configuration -------------------------------------------------
rst_prolog = """
.. _pytest: https://docs.pytest.org
.. |ptx| replace:: *pytest-executable*
.. |exe| replace:: :program:`executable`
.. |pytest| replace:: `pytest`_
.. |yaml| replace:: :file:`test-settings.yaml`
.. |runner| replace:: *runner shell script*
"""


# class DocsonlyMethodDocumenter(autodoc.MethodDocumenter):
#   def format_args(self):
#     return None
#
# autodoc.add_documenter(DocsonlyMethodDocumenter)


class SimpleDocumenter(autodoc.MethodDocumenter):
    objtype = "simple"

    # do not indent the content
    content_indent = ""

    # do not add a header to the docstring
    def add_directive_header(self, sig):
        pass


def setup(app):
    app.add_autodocumenter(SimpleDocumenter)
