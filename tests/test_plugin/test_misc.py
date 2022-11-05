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
"""Tests for the plugin itself."""
from __future__ import annotations

import pytest

from . import assert_outcomes


def test_collect_order(testdir):
    """Check the tests order.

    The default test module functions shall be first. Then the additional test
    modules, and finally the test modules from the parent directories.
    """
    directory = testdir.copy_example("tests/data/collect_order")
    result = testdir.runpytest(directory, "--collect-only")
    result.stdout.re_match_lines(
        [
            "collected 5 items",
            "<TestExecutableModule .*b/test-settings.yaml>",
            "  <Function test_runner>",
            "<Module .*b/a/test_aaa.py>",
            "  <Function test_dummy>",
            "<TestExecutableModule .*z/test-settings.yaml>",
            "  <Function test_runner>",
            "<Module .*z/test_aa.py>",
            "  <Function test_dummy>",
            "<Module .*test_a.py>",
            "  <Function test_dummy>",
        ]
    )


def test_marks_from_yaml(testdir):
    """Test marks from test-settings.yaml."""
    directory = testdir.copy_example("tests/data/test_marks_from_yaml")

    # check tests detection
    result = testdir.runpytest(directory / "tests-inputs")
    assert_outcomes(result, passed=2, skipped=1)

    # select tests not with mark1
    result = testdir.runpytest(
        directory / "tests-inputs", "--collect-only", "-m not mark1"
    )
    assert result.parseoutcomes()["deselected"] == 3


def test_output_directory_already_exists(testdir):
    """Test create_output_dir fixture for existing directory error."""
    directory = testdir.copy_example("tests/data/test_output_dir_fixture")
    result = testdir.runpytest(directory / "tests-inputs")
    # error because directory already exists
    assert_outcomes(result, errors=1)
    result.stdout.fnmatch_lines(
        [
            "E   FileExistsError",
            "",
            "During handling of the above exception, another exception occurred:",
            'E   FileExistsError: the output directory "*" already exists: '
            "either remove it manually or use the --exe-clean-output option to "
            "remove it or use the --exe-overwrite-output to overwrite it",
        ]
    )


def test___init__(testdir):
    """Test error handling when missing __init__.py."""
    testdir.copy_example("tests/data/test___init__")
    result = testdir.runpytest_subprocess()
    assert_outcomes(result, errors=1)
    result.stdout.fnmatch_lines(
        [
            "*/tests-inputs/case2",
            "shall have a __init__.py because test_dummy.py exists in other "
            "directories",
        ]
    )


def test_cli_check_clash(testdir):
    """Test CLI arguments clash."""
    directory = testdir.copy_example("tests/data/test_cli_check")
    result = testdir.runpytest_subprocess(
        directory, "--exe-clean-output", "--exe-overwrite-output"
    )
    result.stderr.fnmatch_lines(
        [
            "ERROR: options --exe-clean-output and --exe-overwrite-output "
            "are not compatible"
        ]
    )


@pytest.mark.parametrize(
    "option_name",
    (
        "--exe-runner",
        "--exe-default-settings",
        "--exe-regression-root",
        "--exe-report-generator",
        "--exe-test-module",
    ),
)
def test_cli_check(testdir, option_name):
    """Test CLI arguments paths."""
    result = testdir.runpytest_subprocess(option_name, "dummy")
    result.stderr.fnmatch_lines(
        [f"ERROR: argument {option_name}: no such file or directory: dummy"]
    )
