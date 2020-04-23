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

"""Tests for run_script."""

import re

import pytest

from pytest_executable.plugin import EXE_RUNNER_NAME
from pytest_executable.script_runner import ScriptExecutionError, ScriptRunner


def test_files_ok(tmp_path):
    """Test that the script execution is OK."""
    script = "echo hello"
    runner = ScriptRunner(EXE_RUNNER_NAME, script, tmp_path)
    runner.run()
    _assertions(tmp_path, runner, script, "hello\n", "")


def test_execution_failure(tmp_path):
    """Test script error."""
    script = "ls non-existing-file"

    error_msg = "execution failure, see the stdout and stderr files in /"
    runner = ScriptRunner(EXE_RUNNER_NAME, script, tmp_path)
    with pytest.raises(ScriptExecutionError, match=error_msg):
        runner.run()

    _assertions(
        tmp_path,
        runner,
        script,
        "",
        "ls: cannot access '?non-existing-file'?: No such file or directory",
    )


def _assertions(tmp_path, runner, script, stdout, stderr_regex):
    script_filename, stdout_filename, stderr_filename = runner._get_filenames()
    # check the content of the script, stdout and stderr files
    with open(tmp_path / script_filename) as file_:
        assert file_.read() == script
    with open(tmp_path / stdout_filename) as file_:
        assert file_.read() == stdout
    with open(tmp_path / stderr_filename) as file_:
        assert re.match(stderr_regex, file_.read())
