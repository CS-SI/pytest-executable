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
"""Tests for the report feature."""
from __future__ import annotations

import shutil
from collections import defaultdict

import pytest
import yaml
from pytest_executable.report import create
from pytest_executable.report import dump
from pytest_executable.report import merge

from . import ROOT_DATA_DIR

DATA_DIR = ROOT_DATA_DIR / "report"


class _TestReport:
    def __init__(self, dir_path: str, message: str) -> None:
        self.path = dir_path
        self.longreprtext = message


class TerminalReporter:
    """Mock of pytest TerminalReporter class."""

    def __init__(self, report_data: list[list[str]]) -> None:
        self.stats: dict[str, list[_TestReport]] = defaultdict(list)
        for status, dir_path, message in report_data:
            self.stats[status] += [_TestReport(dir_path, message)]


# report data with all cases
REPORT_DATA = [
    ["skipped", "root/path", ""],
    ["passed", "root/path", ""],
    ["failed", "root/path", "failure message 0"],
    ["error", "root/path", "error message 0"],
    ["skipped", "root/dir1/path", ""],
    ["passed", "root/dir1/path", ""],
    ["failed", "root/dir1/path", "failure message 1"],
    ["skipped", "root/dir2/path", ""],
    ["passed", "root/dir2/path", ""],
    ["skipped", "root/dir3/path", ""],
    ["skipped", "root/dir3/path", ""],
]


@pytest.mark.parametrize(
    "report_data,expected",
    (
        # tests with one path
        (
            REPORT_DATA[0:4],
            # error priority
            {
                ".": {
                    "status": "error",
                    "messages": ["error message 0", "failure message 0"],
                }
            },
        ),
        (
            REPORT_DATA[4:7],
            # failed priority
            {"dir1": {"status": "failed", "messages": ["failure message 1"]}},
        ),
        (
            REPORT_DATA[7:9],
            # passed if at least one passed
            {"dir2": {"status": "passed", "messages": []}},
        ),
        (
            REPORT_DATA[9:],
            # skipped if all skipped
            {"dir3": {"status": "skipped", "messages": []}},
        ),
        # tests with several paths
        (
            REPORT_DATA,
            # error priority
            {
                ".": {
                    "status": "error",
                    "messages": ["error message 0", "failure message 0"],
                },
                "dir1": {"status": "failed", "messages": ["failure message 1"]},
                "dir2": {"status": "passed", "messages": []},
                "dir3": {"status": "skipped", "messages": []},
            },
        ),
    ),
)
def test_create(report_data, expected):
    """Test create function."""
    assert create(TerminalReporter(report_data)) == expected


@pytest.mark.parametrize(
    "db,expected_db",
    (
        (
            {
                # existing entry is overwritten
                ".": None,
                # new entry is added
                "dir4": None,
            },
            {
                ".": None,
                "dir1": {"status": "failed", "messages": ["failure message 1"]},
                "dir2": {"status": "passed", "messages": []},
                "dir3": {"status": "skipped", "messages": []},
                "dir4": None,
            },
        ),
    ),
)
def test_merge(db, expected_db):
    """Test the merge function."""
    db_path = DATA_DIR / "report_db.yaml"
    new_db = merge(db_path, db)
    assert new_db == expected_db


def test_dump_new(tmp_path):
    """Test dump function without existing db file."""
    report_path = tmp_path / "report_db.yaml"
    dump(report_path, TerminalReporter(REPORT_DATA))

    with report_path.open() as file_:
        db = yaml.safe_load(file_)

    with (DATA_DIR / "report_db.yaml").open() as file_:
        excepted_db = yaml.safe_load(file_)

    assert db == excepted_db


def test_dump_existing(tmp_path):
    """Test dump function with existing db file."""
    expected_path = DATA_DIR / "report_db.yaml"
    report_path = tmp_path / "report_db.yaml"
    shutil.copy(expected_path, report_path)

    # with the same test outcomes, we shall get the same db
    dump(report_path, TerminalReporter(REPORT_DATA))

    with report_path.open() as file_:
        db = yaml.safe_load(file_)

    with expected_path.open() as file_:
        excepted_db = yaml.safe_load(file_)

    assert db == excepted_db
