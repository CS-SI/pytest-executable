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

"""Tests for ScriptRunner."""

import re
from pathlib import Path

import pytest

from pytest_executable.script_runner import ScriptExecutionError, ScriptRunner

from . import ROOT_DATA_DIR

SCRIPT_PATH = ROOT_DATA_DIR / "test_runner_fixture/runner.sh"


def test_execution_with_setting(tmp_path):
    """Test script execution with placeholder replaced."""
    runner = ScriptRunner(SCRIPT_PATH, {"nproc": 100}, tmp_path)
    runner.run()
    _assertions(tmp_path, "echo 100", "100", "")


def test_error_with_missing_setting(tmp_path):
    """Test error when a placeholder cannot be replaced."""
    error_msg = "in .*tests/data/test_runner_fixture/runner.sh: 'nproc' is undefined"
    with pytest.raises(ValueError, match=error_msg):
        ScriptRunner(SCRIPT_PATH, {}, tmp_path)


def test_error_with_unreadable_script(tmp_path):
    """Test error when the script is not readable."""
    error_msg = "cannot read the script .*/bin/bash"
    with pytest.raises(TypeError, match=error_msg):
        ScriptRunner(Path("/bin/bash"), {}, tmp_path)


def test_execution_error(tmp_path):
    """Test error when the script execution fails."""
    error_msg = "execution failure, see the stdout and stderr files in /"
    runner = ScriptRunner(SCRIPT_PATH.parent / "error/runner.sh", {}, tmp_path)
    with pytest.raises(ScriptExecutionError, match=error_msg):
        runner.run()

    _assertions(
        tmp_path,
        "ls non-existing-file",
        "",
        "ls: (?:cannot access )?'?non-existing-file'?: No such file or directory",
    )


def _assertions(tmp_path, script, stdout, stderr_regex):
    # check the content of the script, stdout and stderr files
    with open(tmp_path / "runner.sh") as file_:
        assert file_.read().strip() == script
    with open(tmp_path / "runner.sh.stdout") as file_:
        assert file_.read().strip() == stdout
    with open(tmp_path / "runner.sh.stderr") as file_:
        assert re.match(stderr_regex, file_.read())
