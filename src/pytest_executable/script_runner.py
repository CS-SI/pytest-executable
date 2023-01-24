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
"""Provides the shell script creation and execution routines."""
from __future__ import annotations

import logging
import stat
import subprocess
from pathlib import Path
from typing import cast

import delta
import jinja2

LOG = logging.getLogger(__name__)


class ScriptExecutionError(Exception):
    """Error for script execution."""


class ScriptRunner:
    """Class for creating and running a runner script.

    It can create and execute a shell script from the path to a script with
    placeholders and the settings.

    Attributes:
        path: Path to the script.
        settings: Runner settings from the yaml file.
        workdir: Path to the script working directory.
        STDOUT_EXT: Suffix for the file with the script standard output (class
                    attribute).
        STDERR_EXT: Suffix for the file with the script standard error (class
                    attribute).
        SHELL: Shell used to execute the script (class attribute).
    """

    STDOUT_EXT = "stdout"
    STDERR_EXT = "stderr"
    SHELL = "/usr/bin/env bash"

    def __init__(self, path: Path, settings: dict[str, str], workdir: Path):
        """Docstring just to prevent the arguments to appear in the autodoc.

        Args:
            path: Path to the script.
            settings: Runner settings from the yaml file.
            workdir: Path to the script working directory.
        """
        self.path = path
        self.workdir = workdir
        self.settings = settings
        self._content = self._substitute()

    def _substitute(self) -> str:
        """Return the script contents with replaced placeholders.

        Returns:
            The final script contents.

        Raises:
            TypeError: if the script cannot be processed.
            ValueError: if a placeholder is undefined.
        """
        try:
            template = jinja2.Template(
                self.path.read_text(), undefined=jinja2.StrictUndefined
            )
        except UnicodeDecodeError:
            raise TypeError(f"cannot read the script {self.path}") from None
        try:
            return cast(str, template.render(**self.settings))
        except jinja2.exceptions.UndefinedError as error:
            raise ValueError(f"in {self.path}: {error}") from None

    def run(self) -> int:
        """Execute the script.

        The script is created and executed in the working directory. The stdout
        and stderr of the script are each redirected to files named after the
        script and suffixed with :py:data:`STDOUT_EXT` and :py:data:`STDERR_EXT`.

        Returns:
            The return code of the executed subprocess.

        Raises:
            ScriptExecutionError: If the execution fails.
        """
        filename = self.path.name
        script_path = self.workdir / filename

        # write the script
        with script_path.open("w") as script_file:
            LOG.debug("writing the shell script %s", script_path)
            script_file.write(self._content)

        # make it executable for the user and the group
        permission = stat.S_IMODE(script_path.stat().st_mode)
        script_path.chmod(permission | stat.S_IXUSR | stat.S_IXGRP)

        # redirect the stdout and stderr to files
        stdout = open(self.workdir / f"{filename}.{self.STDOUT_EXT}", "w")
        stderr = open(self.workdir / f"{filename}.{self.STDERR_EXT}", "w")

        LOG.debug("executing the shell script %s", script_path)
        cmd = self.SHELL.split() + [filename]

        timeout = self.settings.get("timeout")

        if timeout is not None:
            # convert to seconds
            timeout = delta.parse(timeout).seconds

        try:
            process = subprocess.run(
                cmd,
                cwd=self.workdir,
                stdout=stdout,
                stderr=stderr,
                check=True,
                timeout=timeout,  # type: ignore
            )
        except subprocess.CalledProcessError:
            # inform about the log files
            raise ScriptExecutionError(
                "execution failure, see the stdout and stderr files in "
                f"{self.workdir}"
            )
        finally:
            stdout.close()
            stderr.close()

        return process.returncode
