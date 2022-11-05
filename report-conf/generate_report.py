#! /usr/bin/env python
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
"""This module generates the test report.

It shall be called from the test output root directory where the tests report
database file is (tests_report_db.yaml). Under the output root directory, it
will create a:
- the index.rst file from the index_template.rst,
- the directory named report that contains the generated report.

In the template index, the summary table and the table of content are inserted.
A line of the summary table contains a case:
- path relative to the output root directory,
- test status (passed, failed, error)
- test messages when the status is not passed
The table of content contains the path to the description.rst files relative to
the output root directory.

This module requires the packages tabulate and sphinx, these could be installed
with the command: conda install tabluate sphinx
"""
from __future__ import annotations

import shutil
import subprocess
import textwrap
from pathlib import Path

import yaml
from tabulate import tabulate

# indentation used in the toc tree of the index template
TOCTREE_INDENTATION = "   "
# name of the directory under the test output directory that will contain the
# generated report
REPORT_OUTPUT_DIRNAME = "report"
# description file name in each test case output directory
DESCRIPTION_FILENAME = "description.rst"
# the directory that contains the current module
DOC_GENERATOR_DIRPATH = Path(__file__).parent
# sphinx documentation builder type
DOC_BUILDER = "html"
# name of the test report database
REPORT_DB_FILENAME = "tests_report_db.yaml"
# template file for creating the index.rst
INDEX_TEMPLATE_RST = "index_template.rst"


def create_summary_table(output_root: Path) -> str:
    """Create the summary table in rst.

    The summary table is sorted alphabetically.

    Args:
        output_root: Path to the test results output directory.

    Returns:
        The summary table string in rst format.
    """
    with (output_root / REPORT_DB_FILENAME).open() as stream:
        report_db = yaml.safe_load(stream)

    report_data: list[tuple[str]] = []
    for case, data in report_db.items():
        messages = "\n".join(data.get("messages", []))
        report_data += [(case, data["status"], messages)]

    return tabulate(
        sorted(report_data), headers=["Case", "Status", "Messages"], tablefmt="rst"
    )


def create_index_rst(output_root: Path) -> None:
    """Create the index.rst.

    Args:
        output_root: Path to the test results output directory.
    """
    # check that the output directory exists
    output_root = Path(output_root).resolve(True)

    # find the paths to the description rst files relatively to the output_root
    description_paths: list[Path] = []
    for path in output_root.glob(f"**/{DESCRIPTION_FILENAME}"):
        description_paths += [path.relative_to(output_root)]

    summary_table = create_summary_table(output_root)

    # the toc tree is sorted alphabetically like the summary table
    toctree_cases = textwrap.indent(
        "\n".join(map(str, sorted(description_paths))), TOCTREE_INDENTATION
    )

    # read the index template
    index_template_path = DOC_GENERATOR_DIRPATH / INDEX_TEMPLATE_RST
    with index_template_path.open() as stream:
        index_rst_template = stream.read()

    # replace the placeholders in the template
    index_rst = index_rst_template.format(
        summary_table=summary_table, toctree_cases=toctree_cases
    )

    # write the final index.rst
    index_path = output_root / "index.rst"
    with index_path.open("w") as stream:
        stream.write(index_rst)


if __name__ == "__main__":
    # common working directory shall be the test output root directory
    output_root = Path.cwd()

    # create the report index.rst
    create_index_rst(output_root)
    # copy the _static directory if it exists
    static_path = DOC_GENERATOR_DIRPATH / "_static"
    if static_path.exists():
        shutil.copytree(static_path, output_root / "_static")

    # command line to build the report
    cmd = (
        f"sphinx-build -b {DOC_BUILDER} -c {DOC_GENERATOR_DIRPATH} "
        f"{output_root} {output_root}/{REPORT_OUTPUT_DIRNAME}"
    )

    # build the report
    subprocess.run(cmd.split(), check=True)
