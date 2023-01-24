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
"""Builtin test module.

This module is automatically executed when a test-settings.yaml file is found.
"""
from __future__ import annotations

from pytest_executable.script_runner import ScriptRunner


def test_runner(runner: ScriptRunner) -> None:
    """Check the runner execution.

    An OK process execution shall return the code 0.

    Args:
        runner: Runner object to be run.
    """
    assert runner.run() == 0
