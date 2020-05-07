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

"""This module contains functions to execute a script in a sub process."""

import logging
import stat
import subprocess
from pathlib import Path
from typing import Any, Dict

import jinja2

LOG = logging.getLogger(__name__)


class ScriptExecutionError(Exception):
    """Error for script execution."""


class ScriptRunner:
    """Base class for creating and running scripts.

    Args:
        filename: Name of the script.
        script: Content of the script.
        exec_dir: Path to the execution directory.
    """

    # extensions for the script related files
    STDOUT_EXT = "stdout"
    STDERR_EXT = "stderr"

    # shell used for executing the shell script
    SHELL = "/usr/bin/env bash"

    def __init__(self, filename: str, script: str, exec_dir: Path):
        self._filename = filename
        self._script = script
        self._exec_dir = exec_dir

    def run(self) -> int:
        """Execute the script.

        The script file is created in the execution directory by dumping the
        contents of the script string. The script stdout and stderr are each
        redirected to files named after the script file prefix and suffixed
        with stdout and stderr.

        Returns:
            The return code of the executed subprocess.

        Raises:
            ScriptExecutionError: If the process fails.
        """
        script_path = self._exec_dir / self._filename

        # write the script
        with script_path.open("w") as script_file:
            LOG.debug("writing the shell script %s", script_path)
            script_file.write(self._script)

        # make it executable for the user and the group
        permission = stat.S_IMODE(script_path.stat().st_mode)
        script_path.chmod(permission | stat.S_IXUSR | stat.S_IXGRP)

        # redirect the stdout and stderr to files
        stdout = open(self._exec_dir / f"{self._filename}.{self.STDOUT_EXT}", "w")
        stderr = open(self._exec_dir / f"{self._filename}.{self.STDERR_EXT}", "w")

        LOG.debug("executing the shell script %s", script_path)
        cmd = self.SHELL.split() + [self._filename]

        try:
            process = subprocess.run(
                cmd, cwd=self._exec_dir, stdout=stdout, stderr=stderr, check=True
            )
        except subprocess.CalledProcessError:
            # inform about the log files
            raise ScriptExecutionError(
                "execution failure, see the stdout and stderr files in "
                f"{self._exec_dir}"
            )
        finally:
            stdout.close()
            stderr.close()

        return process.returncode


def get_final_script(script_path: Path, variables: Dict[str, Any]) -> str:
    """Return the script with replaced placeholders.

    Args:
        script_path: Path to the script.
        variables: Placeholders to be replaced.

    Returns:
        The final script.

    Raises:
        TypeError if the script cannot be processed.
    """
    try:
        template = jinja2.Template(script_path.read_text())
    except UnicodeDecodeError:
        raise TypeError(f"can't read the script {script_path}") from None
    return template.render(**variables)
