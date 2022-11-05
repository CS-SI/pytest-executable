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
"""Entry point into the pytest executable plugin."""
from __future__ import annotations

import logging
import sys
from functools import cmp_to_key
from pathlib import Path

import _pytest
import py
import pytest

from . import report
from .file_tools import create_output_directory
from .file_tools import find_references
from .file_tools import get_mirror_path
from .script_runner import ScriptRunner
from .settings import Settings

LOGGER = logging.getLogger(__name__)

# files to be ignored when creating the output directories symlinks
OUTPUT_IGNORED_FILES = ("__pycache__", "conftest.py", "test-settings.yaml")

# file with the test default settings
SETTINGS_PATH = Path(__file__).parent / "test-settings.yaml"
TEST_MODULE_PATH = Path(__file__).parent / "test_executable.py"

# caches the test case directory path to marks to propagate them to all the
# test modules of a test case
_marks_cache: dict[str, set[str]] = {}


def pytest_addoption(parser):
    """CLI options for the plugin."""
    group = parser.getgroup("executable", "executable testing")

    group.addoption(
        "--exe-runner",
        metavar="PATH",
        help="use the shell script at PATH to run an executable",
    )

    group.addoption(
        "--exe-output-root",
        default="tests-output",
        metavar="PATH",
        help="use PATH as the root directory of the tests output, default: %(default)s",
    )

    group.addoption(
        "--exe-overwrite-output",
        action="store_true",
        help="overwrite existing files in the tests output directories",
    )

    group.addoption(
        "--exe-clean-output",
        action="store_true",
        help="clean the tests output directories before executing the tests",
    )

    group.addoption(
        "--exe-regression-root",
        metavar="PATH",
        help="use PATH as the root directory with the references for the "
        "regression testing",
    )

    group.addoption(
        "--exe-default-settings",
        default=SETTINGS_PATH,
        metavar="PATH",
        help="use PATH as the yaml file with the global default test settings instead "
        "of the built-in ones",
    )

    group.addoption(
        "--exe-test-module",
        default=TEST_MODULE_PATH,
        metavar="PATH",
        help="use PATH as the default test module",
    )

    group.addoption(
        "--exe-report-generator",
        metavar="PATH",
        help="use PATH as the script to generate the test report",
    )

    # change default traceback settings to get only the message without the
    # traceback
    term_rep_options = parser.getgroup("terminal reporting").options
    tb_option = next(
        option for option in term_rep_options if option.names() == ["--tb"]
    )
    tb_option.default = "line"


def pytest_sessionstart(session):
    """Check the CLI arguments and resolve their paths."""
    option = session.config.option

    # check options clash
    if option.exe_clean_output and option.exe_overwrite_output:
        msg = "options --exe-clean-output and --exe-overwrite-output are not compatible"
        raise pytest.UsageError(msg)

    # check paths are valid
    for option_name in (
        "exe_runner",
        "exe_test_module",
        "exe_default_settings",
        "exe_regression_root",
        "exe_report_generator",
    ):
        path = getattr(option, option_name)
        try:
            path = Path(path).resolve(True)
        except FileNotFoundError:
            msg = (
                f"argument --{option_name.replace('_', '-')}: "
                f"no such file or directory: {path}"
            )
            raise pytest.UsageError(msg)
        except TypeError:
            # path is None, i.e. no option is defined
            pass
        else:
            # overwrite the option with the resolved path
            setattr(option, option_name, path)

    # convert remaining option with pat
    option.exe_output_root = Path(option.exe_output_root).resolve()


def _get_parent_path(fspath: py.path.local) -> Path:
    """Return the resolved path to a parent directory.

    Args:
        fspath: Path object from pytest.

    Returns:
        Resolved path to the parent directory of the given pat.
    """
    return Path(fspath).parent.resolve(True)


@pytest.fixture(scope="module")
def create_output_tree(request):
    """Fixture to create and return the path to the output directory tree."""
    option = request.config.option
    parent_path = _get_parent_path(request.node.fspath)
    output_path = get_mirror_path(parent_path, option.exe_output_root)

    try:
        create_output_directory(
            parent_path,
            output_path,
            not option.exe_overwrite_output,
            option.exe_clean_output,
            OUTPUT_IGNORED_FILES,
        )
    except FileExistsError:
        msg = (
            f'the output directory "{output_path}" already exists: either '
            "remove it manually or use the --exe-clean-output option to remove "
            "it or use the --exe-overwrite-output to overwrite it"
        )
        raise FileExistsError(msg)


@pytest.fixture(scope="module")
def output_path(request):
    """Fixture to return the path to the output directory."""
    return get_mirror_path(
        _get_parent_path(request.node.fspath), request.config.option.exe_output_root
    )


def _get_settings(config: _pytest.config.Config, path: py.path.local) -> Settings:
    """Return the settings from global and local test-settings.yaml.

    Args:
        config: Config from pytest.
        path: Path to a test case directory.

    Returns:
        The settings from the test case yaml.
    """
    return Settings.from_local_file(
        Path(config.option.exe_default_settings),
        _get_parent_path(path) / SETTINGS_PATH.name,
    )


@pytest.fixture(scope="module")
def tolerances(request):
    """Fixture that provides the tolerances from the settings."""
    return _get_settings(request.config, request.node.fspath).tolerances


@pytest.fixture(scope="module")
def runner(request, create_output_tree, output_path):
    """Fixture to execute the runner script."""
    runner_path = request.config.option.exe_runner
    if runner_path is None:
        pytest.skip("no runner provided with --exe-runner")

    settings = _get_settings(request.config, request.node.fspath).runner
    settings["output_path"] = output_path

    return ScriptRunner(runner_path, settings, output_path)


def _get_regression_path(
    config: _pytest.config.Config, fspath: py.path.local
) -> Path | None:
    """Return the path to the reference directory of a test case.

    None is returned if --exe-regression-root is not passed to the CLI.

    Args:
        config: Config from pytest.
        fspath: Path to a test case directory.

    Returns:
        The path to the reference directory of the test case or None.
    """
    regression_path = config.option.exe_regression_root
    if regression_path is None:
        return None
    return get_mirror_path(_get_parent_path(fspath), regression_path)


@pytest.fixture(scope="module")
def regression_path(request):
    """Fixture to return the path of a test case under the references tree."""
    regression_path = _get_regression_path(request.config, request.node.fspath)
    if regression_path is None:
        pytest.skip(
            "no tests references root directory provided to --exe-regression-root"
        )
    return regression_path


def pytest_generate_tests(metafunc):
    """Create the regression_file_path parametrized fixture.

    Used for accessing the references files.

    If --exe-regression-root is not set then no reference files will be provided.
    """
    if "regression_file_path" not in metafunc.fixturenames:
        return

    # result absolute and relative file paths to be provided by the fixture parameter
    # empty means skip the test function that use the fixture
    file_paths = []

    regression_path = _get_regression_path(metafunc.config, metafunc.definition.fspath)

    if regression_path is not None:
        settings_path = metafunc.definition.fspath
        settings = _get_settings(metafunc.config, settings_path)

        if settings.references:
            file_paths = find_references(regression_path, settings.references)

    metafunc.parametrize(
        "regression_file_path",
        file_paths,
        scope="function",
        ids=list(map(str, [f.relative for f in file_paths])),
    )


def pytest_collect_file(parent, path):
    """Collect test cases defined with a yaml file."""
    if path.basename != SETTINGS_PATH.name:
        return
    if hasattr(TestExecutableModule, "from_parent"):
        return TestExecutableModule.from_parent(parent, fspath=path)
    else:
        return TestExecutableModule(path, parent)


def pytest_configure(config: _pytest.config.Config) -> None:
    """Register the possible markers and change default error display.

    Display only the last error line without the traceback.
    """
    config.addinivalue_line(
        "markers", 'slow: marks tests as slow (deselect with -m "not slow")'
    )

    # show only the last line with the error message when displaying a
    # traceback
    if config.option.tbstyle == "auto":
        config.option.tbstyle = "line"


class TestExecutableModule(pytest.Module):
    """Collector for tests defined with a yaml file."""

    def _getobj(self):
        """Override the base class method.

        To swap the yaml file with the test module.
        """
        test_module_path = Path(self.config.option.exe_test_module)

        # prevent python from using the module cache, otherwise the module
        # object will be the same for all the tests
        try:
            del sys.modules[test_module_path.stem]
        except KeyError:
            pass

        # backup the attribute before a temporary override of it
        fspath = self.fspath
        self.fspath = py.path.local(test_module_path)
        module = self._importtestmodule()

        # restore the backuped up attribute
        self.fspath = fspath

        # set the test case marks from test-settings.yaml
        settings = _get_settings(self.config, fspath)

        # store the marks for applying them later
        if settings.marks:
            _marks_cache[fspath.dirname] = settings.marks

        return module


def pytest_exception_interact(node, call, report):
    """Change exception display to only show the test path and error message.

    Avoid displaying the test file path and the Exception type.
    """
    excinfo = call.excinfo
    if excinfo.typename == "CollectError" and str(excinfo.value).startswith(
        "import file mismatch:\n"
    ):
        # handle when a custom test script is used in more than one test case with
        # the same name
        dirname = node.fspath.dirname
        filename = node.fspath.basename
        report.longrepr = (
            f"{dirname}\nshall have a __init__.py because {filename} "
            "exists in other directories"
        )
    else:
        report.longrepr.reprcrash = f"{report.nodeid}: {excinfo.value}"


def pytest_collection_modifyitems(items: list[_pytest.nodes.Item]) -> None:
    """Change the tests execution order.

    Such that:
    - the tests in parent directories are executed after the tests in children
      directories
    - in a test case directory, the yaml defined tests are executed before the
      others
    """
    items.sort(key=cmp_to_key(_sort_parent_last))
    items.sort(key=cmp_to_key(_sort_yaml_first))
    _set_marks(items)


def _sort_yaml_first(item_1: _pytest.nodes.Item, item_2: _pytest.nodes.Item) -> int:
    """Sort yaml item first vs module at or below yaml parent directory."""
    path_1 = Path(item_1.fspath)
    path_2 = Path(item_2.fspath)
    if path_1 == path_2 or path_1.suffix == path_2.suffix:
        return 0
    if path_2.suffix == ".yaml" and (path_2.parent in path_1.parents):
        return 1
    if path_1.suffix == ".yaml" and (path_1.parent in path_2.parents):
        return -1
    return 0


def _sort_parent_last(item_1: _pytest.nodes.Item, item_2: _pytest.nodes.Item) -> int:
    """Sort item in parent directory last."""
    dir_1 = Path(item_1.fspath).parent
    dir_2 = Path(item_2.fspath).parent
    if dir_1 == dir_2:
        return 0
    if dir_2 in dir_1.parents:
        return -1
    return 1


def _set_marks(items: list[_pytest.nodes.Item]) -> None:
    """Set the marks to all the test functions of a test case."""
    for dirname, marks in _marks_cache.items():
        for item in items:
            if Path(dirname) in Path(item.fspath).parents:
                for mark in marks:
                    item.add_marker(mark)


def pytest_terminal_summary(
    terminalreporter: _pytest.terminal.TerminalReporter,
    config: _pytest.config.Config,
) -> None:
    """Create the custom report.

    In the directory that contains the report generator, the report database is created
    and the report generator is called.
    """
    # path to the report generator
    reporter_path = config.option.exe_report_generator
    if reporter_path is None:
        return

    if not terminalreporter.stats:
        # no test have been run thus no report to create or update
        return

    terminalreporter.write_sep("=", "starting report generation")

    try:
        report.generate(reporter_path, config.option.exe_output_root, terminalreporter)
    except Exception as e:
        terminalreporter.write_line(str(e), red=True)
        terminalreporter.write_sep("=", "report generation failed", red=True)
    else:
        terminalreporter.write_sep("=", "report generation done")
