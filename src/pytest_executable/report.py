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
"""Provide the report database dumper and report generation."""
from __future__ import annotations

import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any
from typing import Dict

from _pytest.terminal import TerminalReporter

from .yaml_helper import YamlHelper

YAML_HELPER = YamlHelper(Path(__file__).parent / "report-db-schema.yaml")

REPORT_DB_FILENAME = "tests_report_db.yaml"
REPORT_DIRNAME = "report"

ReportDBType = Dict[str, Dict[str, Any]]


def create(terminalreporter: TerminalReporter) -> ReportDBType:
    """Create the report database.

    A test case is errored if at least one test function is error. A test case
    is failed if at least one test function is failed. A test case is skipped
    if all the test functions are skipped. Otherwise, it is passed.

    All the error and failure messages are listed for a given path.

    Args:
        terminalreporter: Pytest terminal reporter.

    Returns:
        The report database.
    """
    report_db: ReportDBType = defaultdict(dict)
    seen_dirs: set[str] = set()

    for status in ("error", "failed", "passed", "skipped"):
        stats = terminalreporter.stats.get(status, [])
        for test_report in stats:
            try:
                path = test_report.path
            except AttributeError:
                path = test_report.fspath
            path_from_root = Path(*Path(path).parts[1:])
            dir_path = str(path_from_root.parent)
            db_entry = report_db[dir_path]
            messages = db_entry.setdefault("messages", [])
            if status in ("error", "failed"):
                messages += [test_report.longreprtext]
            if dir_path in seen_dirs:
                continue
            seen_dirs.add(dir_path)
            db_entry["status"] = status

    return dict(report_db)


def merge(db_path: Path, new_db: ReportDBType) -> ReportDBType:
    """Merge a report database into an existing database on disk.

    The entries in db_path but not in new_db are left untouched. The entries in
    both are overwritten with the ones in new_db. The entries only in new_db
    are added.

    Args:
        db_path: Path to a database file.
        new_db: Database to be merged from.

    Returns:
        The merged database.
    """
    merged_db = YAML_HELPER.load(db_path)
    merged_db.update(new_db)
    return merged_db


def dump(report_db_path: Path, terminalreporter: TerminalReporter) -> None:
    """Dump the report database.

    If the database file already exists then new test results are merged with
    the ones in the file.

    The database yaml file have the following format:

    path/to/a/test/case:
      status: the test case status among error, failure, passed and skipped
      messages: list of error and failure messages for all the test functions
                of the test case

    Args:
        report_db_path: Path to the report db file.
        terminalreporter: Pytest terminal reporter.
    """
    report_db = create(terminalreporter)

    if report_db_path.is_file():
        report_db = merge(report_db_path, report_db)

    YAML_HELPER.dump(report_db, report_db_path.open("w"))


def generate(
    script_path: str, output_root: Path, terminalreporter: TerminalReporter
) -> None:
    """Generate the report in the output root.

    The directory that contains script_path is shallow copied in output_root,
    the report is created there.

    Args:
        script_path: Path to the reporter generator script.
        output_root: Path to the test results root directory.
        terminalreporter: Pytest terminal reporter.
    """
    # check that the report generator script is there
    reporter_path = Path(script_path).resolve(True)

    # write the report database
    dump(output_root / REPORT_DB_FILENAME, terminalreporter)

    # generate the report
    subprocess.run(str(reporter_path), cwd=output_root, check=True, shell=True)
