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
"""Test the report feature."""
from __future__ import annotations

import stat
from pathlib import Path

import pytest

# deal with old pytest not having no_re_match_line
# TODO: remove this once old pytest is no longer supported
OLD_PYTEST = pytest.__version__ < "5.3.0"


def test_report_no_report_generator(testdir):
    """Test no report title in the output when no report option is used."""
    directory = testdir.copy_example("tests/data/test_report")
    result = testdir.runpytest(directory / "tests-inputs")
    # skip runner because no --exe-runner
    result.assert_outcomes(skipped=1)
    if OLD_PYTEST:
        assert "report generation" not in result.stdout.str()
    else:
        result.stdout.no_re_match_line("report generation")


def fix_execute_permission(script_path: str) -> None:
    """Pytest testdir fixture does not copy the execution bit."""
    path = Path(script_path)
    permission = stat.S_IMODE(path.stat().st_mode)
    path.chmod(permission | stat.S_IXUSR)


def test_report_generator_internal_error(testdir):
    """Test error when generator has internal error."""
    directory = testdir.copy_example("tests/data/test_report")
    generator_path = directory / "report/generator-ko.sh"
    fix_execute_permission(generator_path)
    result = testdir.runpytest(
        directory / "tests-inputs",
        "--exe-report-generator",
        generator_path,
    )
    # skip runner because no --exe-runner
    result.assert_outcomes(skipped=1)
    result.stdout.re_match_lines(
        [
            ".*starting report generation",
            "Command '.*/test_report_generator_internal_error0/report/generator-ko.sh' "
            "returned non-zero exit status 1.",
            ".*report generation failed",
        ]
    )


def test_report_generator_ok(testdir):
    """Test error when generator work ok."""
    directory = testdir.copy_example("tests/data/test_report")
    generator_path = directory / "report/generator.sh"
    fix_execute_permission(generator_path)
    result = testdir.runpytest(
        directory / "tests-inputs", "--exe-report-generator", generator_path
    )
    # skip runner because no --exe-runner
    result.assert_outcomes(skipped=1)
    result.stdout.re_match_lines(
        [".*starting report generation", ".*report generation done"]
    )


def test_no_test_no_report(testdir):
    """Test no report generator is called when there is no test run."""
    directory = testdir.copy_example("tests/data/test_report")
    generator_path = directory / "report/generator.sh"
    fix_execute_permission(generator_path)
    result = testdir.runpytest(
        directory / "tests-inputs/empty-case", "--exe-report-generator", generator_path
    )
    result.assert_outcomes()
    if OLD_PYTEST:
        assert "report generation" not in result.stdout.str()
    else:
        result.stdout.no_re_match_line("report generation")
