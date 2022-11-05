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
"""Tests for the plugin fixtures."""
from __future__ import annotations

from . import assert_outcomes


def test_tolerances_fixture(testdir):
    """Test tolerances fixture from test-settings.yaml."""
    directory = testdir.copy_example("tests/data/test_tolerances_fixture")
    result = testdir.runpytest(directory / "tests-inputs")
    # skip runner because no --exe-runner
    # pass fixture
    assert_outcomes(result, passed=1, skipped=1)


def test_regression_path_fixture(testdir):
    """Test regression_path fixture."""
    directory = testdir.copy_example("tests/data/test_regression_path_fixture")
    result = testdir.runpytest(
        directory / "tests-inputs", "--exe-regression-root", directory / "references"
    )
    # skip runner because no --exe-runner
    # pass fixture test
    assert_outcomes(result, skipped=1, passed=1)


def test_regression_path_fixture_no_regression_root(testdir):
    """Test skipping regression_path fixture without --exe-regression-root option."""
    directory = testdir.copy_example("tests/data/test_regression_path_fixture")
    result = testdir.runpytest(directory / "tests-inputs")
    # skip runner because no --exe-runner
    assert_outcomes(result, skipped=2)


def test_regression_file_path_fixture_no_regression_root(testdir):
    """Test skipping regression_file_path fixture without --exe-regression-root."""
    directory = testdir.copy_example("tests/data/test_regression_file_path_fixture")
    result = testdir.runpytest(directory / "tests-inputs/case-no-references")
    assert_outcomes(result, skipped=1)


def test_regression_file_path_fixture_no_references(testdir):
    """Test skipping regression_file_path fixture whitout references."""
    directory = testdir.copy_example("tests/data/test_regression_file_path_fixture")
    result = testdir.runpytest(
        directory / "tests-inputs/case-no-references",
        "--exe-regression-root",
        directory / "references",
    )
    assert_outcomes(result, skipped=1)


RUNNER_DATA_DIR = "tests/data/test_runner_fixture"


def test_runner_fixture_no_runner(testdir):
    """Test skipping runner fixture without runner."""
    directory = testdir.copy_example(RUNNER_DATA_DIR)
    result = testdir.runpytest(directory / "tests-inputs/case-local-settings")
    assert_outcomes(result, skipped=1)


def test_runner_fixture_with_local_settings(testdir):
    """Test runner fixture with placeholder from local test settings."""
    directory = testdir.copy_example(RUNNER_DATA_DIR)
    result = testdir.runpytest(
        directory / "tests-inputs/case-local-settings",
        "--exe-runner",
        directory / "runner.sh",
    )
    assert_outcomes(result, passed=1)
    stdout = (
        (directory / "tests-output/case-local-settings/runner.sh.stdout")
        .open()
        .read()
        .strip()
    )
    assert stdout == "100"


def test_runner_not_script(testdir):
    """Test error when the runner is not a text script."""
    directory = testdir.copy_example(RUNNER_DATA_DIR)
    result = testdir.runpytest(
        directory / "tests-inputs/case-local-settings",
        "--exe-runner",
        "/bin/bash",
    )
    assert_outcomes(result, errors=1)
    result.stdout.fnmatch_lines(["E   TypeError: cannot read the script */bin/bash"])


def test_runner_fixture_with_global_settings(testdir):
    """Test runner fixture with nproc from default settings."""
    directory = testdir.copy_example(RUNNER_DATA_DIR)
    result = testdir.runpytest(
        directory / "tests-inputs/case-global-settings",
        "--exe-runner",
        directory / "runner.sh",
        "--exe-default-settings",
        directory / "settings.yaml",
    )
    assert_outcomes(result, passed=1)
    stdout = (
        (directory / "tests-output/case-global-settings/runner.sh.stdout")
        .open()
        .read()
        .strip()
    )
    assert stdout == "100"


def test_runner_error_with_undefined_placeholder(testdir):
    """Test error with runner fixture when a placeholder is not replaced."""
    directory = testdir.copy_example(RUNNER_DATA_DIR)
    result = testdir.runpytest(
        directory / "tests-inputs/case-global-settings",
        "--exe-runner",
        directory / "runner.sh",
    )
    assert_outcomes(result, errors=1)
    result.stdout.fnmatch_lines(
        ["E   ValueError: in */runner.sh: 'nproc' is undefined"]
    )
