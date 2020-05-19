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

"""Provides the shell script creation and execution."""

import logging
import stat
import subprocess
from pathlib import Path
from typing import Dict

import jinja2

LOG = logging.getLogger(__name__)


class ScriptExecutionError(Exception):
    """Error for script execution."""


class ScriptRunner:
    """Class for creating and running scripts.

    Args:
        path: Path to the script.
        settings: Variables to replace the placeholders.
        exec_path: Path to the execution directory.
    """

    # extensions for the script related files
    STDOUT_EXT = "stdout"
    STDERR_EXT = "stderr"

    # shell used for executing the shell script
    SHELL = "/usr/bin/env bash"

    def __init__(self, path: Path, settings: Dict[str, str], exec_path: Path):
        self._path = Path(path).resolve(True)
        self._content = self._substitute(settings)
        self._exec_path = exec_path

    def _substitute(self, variables: Dict[str, str]) -> str:
        """Return the script contents with replaced placeholders.

        Args:
            variables: Variables to replace the placeholders.

        Returns:
            The final script contents.

        Raises:
            TypeError if the script cannot be processed.
            ValueError is a placeholder is undefined.
        """
        try:
            template = jinja2.Template(
                self._path.read_text(), undefined=jinja2.StrictUndefined
            )
        except UnicodeDecodeError:
            raise TypeError(f"cannot read the script {self._path}") from None
        try:
            return template.render(**variables)
        except jinja2.exceptions.UndefinedError as error:
            raise ValueError(f"in {self._path}: {error}") from None

    def run(self) -> int:
        """Execute the script.

        The script file is created in the execution directory by dumping the
        contents of the script. The script stdout and stderr are each
        redirected to files named after the script file prefix and suffixed
        with stdout and stderr.

        Returns:
            The return code of the executed subprocess.

        Raises:
            ScriptExecutionError: If the process fails.
        """
        filename = self._path.name
        script_path = self._exec_path / filename

        # write the script
        with script_path.open("w") as script_file:
            LOG.debug("writing the shell script %s", script_path)
            script_file.write(self._content)

        # make it executable for the user and the group
        permission = stat.S_IMODE(script_path.stat().st_mode)
        script_path.chmod(permission | stat.S_IXUSR | stat.S_IXGRP)

        # redirect the stdout and stderr to files
        stdout = open(self._exec_path / f"{filename}.{self.STDOUT_EXT}", "w")
        stderr = open(self._exec_path / f"{filename}.{self.STDERR_EXT}", "w")

        LOG.debug("executing the shell script %s", script_path)
        cmd = self.SHELL.split() + [filename]

        try:
            process = subprocess.run(
                cmd, cwd=self._exec_path, stdout=stdout, stderr=stderr, check=True
            )
        except subprocess.CalledProcessError:
            # inform about the log files
            raise ScriptExecutionError(
                "execution failure, see the stdout and stderr files in "
                f"{self._exec_path}"
            )
        finally:
            stdout.close()
            stderr.close()

        return process.returncode
