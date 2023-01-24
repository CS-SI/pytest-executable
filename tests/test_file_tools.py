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
"""Tests for the file tools."""
from __future__ import annotations

import os
from pathlib import Path

import pytest
from pytest_executable.file_tools import create_output_directory
from pytest_executable.file_tools import find_references
from pytest_executable.file_tools import get_mirror_path

from . import ROOT_DATA_DIR

DATA_DIR = ROOT_DATA_DIR / "shallow_dir_copy"


@pytest.fixture(scope="module")
def shared_tmp_path(tmp_path_factory):
    """Shared tmp_path fixture for the current module."""
    return tmp_path_factory.mktemp("dummy")


def test_non_existing_destination(shared_tmp_path):
    """Test shallow directory copy with non-existing destination."""
    _helper(shared_tmp_path, True, False)


def test_existing_destination_clean(shared_tmp_path):
    """Test clean shallow directory copy with existing destination."""
    # this test shall be executed after test_non_existing_destination
    _helper(shared_tmp_path, True, True)


def test_existing_destination_ko(shared_tmp_path):
    """Test errors."""
    # force creation for using with xdist
    _helper(shared_tmp_path, True, True)
    with pytest.raises(FileExistsError):
        _helper(shared_tmp_path, True, False)


def test_existing_destination_overwrite(shared_tmp_path):
    """Test overwrite shallow directory copy with existing destination."""
    _helper(shared_tmp_path, False, False)


def _helper(shared_tmp_path, check, overwrite):
    create_output_directory(
        DATA_DIR / "src_dir",
        shared_tmp_path / "dst_dir",
        check,
        overwrite,
        ["file-to-ignore"],
    )
    _compare_directory_trees(
        DATA_DIR / "dst_dir", shared_tmp_path / "dst_dir/data/shallow_dir_copy/src_dir"
    )


def _compare_directory_trees(exp_dir, dst_dir):
    for exp_entries, dst_entries in zip(os.walk(exp_dir), os.walk(dst_dir)):
        # check the names of the subdirectories and the files
        assert dst_entries[1:] == exp_entries[1:]

        # check the directories type
        assert [Path(dst_entries[0], e).is_dir() for e in dst_entries[1]] == [
            Path(exp_entries[0], e).is_dir() for e in exp_entries[1]
        ]

        # check the symlinks type
        assert [Path(dst_entries[0], e).is_symlink() for e in dst_entries[2]] == [
            Path(exp_entries[0], e).is_symlink() for e in exp_entries[2]
        ]

        # check symlinks pointed path
        assert [Path(dst_entries[0], e).resolve() for e in dst_entries[2]] == [
            Path(exp_entries[0], e).resolve() for e in exp_entries[2]
        ]


@pytest.fixture
def _tmp_path(tmp_path):
    cwd = Path.cwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(cwd)


def test_get_mirror_path_ok(_tmp_path):
    """Test get_mirror_path."""
    path_from = _tmp_path / "c/d/e"
    path_from.mkdir(parents=True)
    assert get_mirror_path(path_from, _tmp_path / "x/y") == _tmp_path / "x/y/d/e"
    assert get_mirror_path(path_from, Path("/x/y")) == Path("/x/y/d/e")

    # with common parents
    path_from = _tmp_path / "a/b/c/d/e"
    path_from.mkdir(parents=True)
    assert (
        get_mirror_path(path_from, _tmp_path / "a/b/x/y") == _tmp_path / "a/b/x/y/d/e"
    )


def test_get_mirror_path_ko(tmp_path):
    """Test get_mirror_path failures."""
    msg = (
        f"the current working directory {Path.cwd()} shall be a parent directory of "
        f"the inputs directory {tmp_path}"
    )
    with pytest.raises(ValueError, match=msg):
        get_mirror_path(tmp_path, "")


def test_find_references():
    """Test find_references."""
    data_dir = ROOT_DATA_DIR / "find_references"
    file_paths = find_references(data_dir / "ref-dir", ["**/*.prf"])
    abs_paths = [f.absolute for f in file_paths]
    assert abs_paths == [data_dir / "ref-dir/0/1.prf", data_dir / "ref-dir/0/dir/2.prf"]
    rel_paths = [f.relative for f in file_paths]
    assert rel_paths == [Path("0/1.prf"), Path("0/dir/2.prf")]
    # empty case
    assert not find_references(data_dir / "ref-dir", ["**/*.dummy"])
