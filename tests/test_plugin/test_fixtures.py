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

"""Tests for the plugin itself."""


def test_tolerances_fixture(testdir):
    """Test tolerances fixture from test_case.yaml."""
    directory = testdir.copy_example("tests/data/test_tolerances_fixture")
    result = testdir.runpytest(directory / "tests-inputs")
    # skip runner because no --runner
    # fail logs because no executable.std*
    # pass fixture
    result.assert_outcomes(passed=1, skipped=1, failed=1)


def test_regression_path_fixture(testdir):
    """Test regression_path fixture."""
    directory = testdir.copy_example("tests/data/test_regression_path_fixture")
    result = testdir.runpytest(
        directory / "tests-inputs", "--regression-root", directory / "references"
    )
    # skip runner because no --runner
    # fail logs because no executable.std*
    # pass fixture test
    result.assert_outcomes(skipped=1, failed=1, passed=1)


def test_regression_path_fixture_no_regression_root(testdir):
    """Test skipping regression_path fixture without --regression-root option."""
    directory = testdir.copy_example("tests/data/test_regression_path_fixture")
    result = testdir.runpytest(directory / "tests-inputs")
    # skip runner because no --runner
    # fail logs because no executable.std*
    result.assert_outcomes(skipped=2, failed=1)


def test_regression_file_path_fixture_no_regression_root(testdir):
    """Test skipping regression_file_path fixture without --regression-root option."""
    directory = testdir.copy_example("tests/data/test_regression_file_path_fixture")
    result = testdir.runpytest(directory / "tests-inputs/case-no-references")
    # skip runner because no --runner
    # fail logs because no executable.std*
    result.assert_outcomes(skipped=1, failed=1)


def test_regression_file_path_fixture_no_references(testdir):
    """Test skipping regression_file_path fixture whitout references."""
    directory = testdir.copy_example("tests/data/test_regression_file_path_fixture")
    result = testdir.runpytest(
        directory / "tests-inputs/case-no-references",
        "--regression-root",
        directory / "references",
    )
    # skip runner because no --runner
    # fail logs because no executable.std*
    result.assert_outcomes(skipped=1, failed=1)


def test_runner_fixture_no_runner(testdir):
    """Test runner fixture without runner."""
    directory = testdir.copy_example("tests/data/test_runner_fixture")
    result = testdir.runpytest(directory / "tests-inputs/case")
    # skip runner because no --runner
    # fail logs because no executable.std*
    result.assert_outcomes(skipped=1, failed=1)


def test_runner_fixture_with_test_case_nproc(testdir):
    """Test runner fixture with custom nproc from test case settings."""
    directory = testdir.copy_example("tests/data/test_runner_fixture")
    result = testdir.runpytest(
        directory / "tests-inputs/case_nproc", "--runner", directory / "runner.sh"
    )
    # fail runner because runner is not runnable
    # fail logs because no executable.std*
    result.assert_outcomes(failed=2)
    run_executable_script = (
        (directory / "tests-output/case_nproc/run_executable.sh").open().read()
    )
    assert " -np 100 " in run_executable_script


def test_runner_fixture_with_global_nproc(testdir):
    """Test runner fixture with custom nproc from default settings."""
    directory = testdir.copy_example("tests/data/test_runner_fixture")
    result = testdir.runpytest(
        directory / "tests-inputs/case",
        "--runner",
        directory / "runner.sh",
        "--default-settings",
        directory / "settings.yaml",
    )
    # fail runner because runner is not runnable
    # fail logs because no executable.std*
    result.assert_outcomes(failed=2)
    run_executable_script = (
        (directory / "tests-output/case/run_executable.sh").open().read()
    )
    assert " -np 100 " in run_executable_script


def test_runner_not_script(testdir):
    """Test error when the runner is not a script."""
    directory = testdir.copy_example("tests/data/test_runner_fixture")
    result = testdir.runpytest(
        directory / "tests-inputs/case", "--runner", "/bin/bash",
    )
    # fail runner because runner is not runnable
    # fail logs because no executable.std*
    result.assert_outcomes(error=1, failed=1)
    result.stdout.fnmatch_lines(["E   TypeError: can't read the script */bin/bash"])
