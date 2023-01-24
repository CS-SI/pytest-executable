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
"""Output directory tree creation functions."""
from __future__ import annotations

import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

LOG = logging.getLogger(__name__)


@dataclass
class FilePath:
    """Relative and absolute file path.

    Attributes:
        relative: Relative path to a file.
        absolute: Absolute path to a file.
    """

    absolute: Path
    relative: Path


def get_mirror_path(path_from: Path, path_to: Path) -> Path:
    """Return the mirror path from a path to another one.

    The mirrored path is determined from the current working directory (cwd)
    and the path_from. The path_from shall be under the cwd. The mirrored
    relative path is the part of path_from that has no common ancestor with
    path_to, without its first parent. For example, given cwd, if path_from is
    c/d/e and path_to is /x/y, then it returns /x/y/d/e (no common ancestor
    between path_from and path_to). If path_to is c/x/y, then cwd/c/x/y/e is
    returned.

    Args:
        path_from: Path to be mirrored from.
        path_to: Root path to be mirrored to.

    Returns:
        Mirror path.

    Raises:
        ValueError: If path_from is not under the cwd.
    """
    cwd = str(Path.cwd().resolve())
    path_from = path_from.resolve(True)

    try:
        relative_from = path_from.relative_to(cwd)
    except ValueError:
        # re-raise with better message
        msg = (
            f"the current working directory {cwd} shall be a parent directory of "
            f"the inputs directory {path_from}"
        )
        raise ValueError(msg)

    # number of directory levels to skip for determining the mirrored relative
    # path
    offset = 1

    try:
        relative_to = path_to.relative_to(cwd)
    except ValueError:
        pass
    else:
        # find the common path part between from and to
        for part_from, part_to in zip(relative_from.parts, relative_to.parts):
            if part_from == part_to:
                offset += 1

    return path_to.joinpath(*relative_from.parts[offset:])


def find_references(ref_dir: Path, ref_files: Iterable[str]) -> list[FilePath]:
    """Return the paths to the references files.

    Args:
        ref_dir: Path to a case directory under the references tree.
        ref_files: Path patterns to the references files.

    Returns:
        Absolute and relative paths from a reference case directory to the
        reference files.
    """
    abs_paths: list[Path] = []
    for ref in ref_files:
        abs_paths += ref_dir.glob(ref)

    if not abs_paths:
        return []

    file_paths: list[FilePath] = []
    for abs_path in abs_paths:
        rel_path = abs_path.relative_to(ref_dir)
        file_paths += [FilePath(abs_path, rel_path)]

    return file_paths


def create_output_directory(
    src_dir: Path,
    dst_dir: Path,
    check_dst: bool,
    clean_dst: bool,
    ignored_files: Iterable[str],
) -> None:
    """Create a directory copy with symbolic links.

    The destination directory is created if it does not exist or if clean_dst
    is true. Only the specified input files will be symlinked, the other files
    will be ignored.

    Args:
        src_dir: Path to the source directory.
        dst_dir: Path to the destination directory.
        check_dst: Whether to check that destination exists.
        clean_dst: Whether to remove an existing destination.
        ignored_files: Files to be ignored when creating the destination
        directory.

    Raises:
        FileExistsError: If the destination directory exists when check_dst is
        true and clean_dst is false.
    """
    # destination checking: force erasing or fail
    if check_dst and dst_dir.is_dir():
        if clean_dst:
            LOG.debug("removing output directory %s", dst_dir)
            shutil.rmtree(dst_dir)
        else:
            raise FileExistsError

    LOG.debug("creating a shallow copy from %s to %s", src_dir, dst_dir)
    _shallow_dir_copy(src_dir, dst_dir, ignored_files)


def _shallow_dir_copy(
    src_dir: Path, dst_dir: Path, ignored_files: Iterable[str]
) -> None:
    """Shallow copy a directory tree.

    Directories are duplicated, files are symlinked. The destination directory
    shall not exist and will be created.

    Args:
        src_dir: Path to the source directory.
        dst_dir: Path to the destination directory.
        ignored_files: Files to be ignored.
    """
    dst_dir.mkdir(parents=True, exist_ok=True)
    for src_entry in src_dir.iterdir():
        dst_entry = dst_dir / src_entry.name
        if src_entry.name in ignored_files:
            pass
        elif src_entry.is_dir():
            # directories are not symlinked but created such that we can not modify a
            # child file by accident
            _shallow_dir_copy(src_entry, dst_entry, ignored_files)
        else:
            # symlink files, first removing an already existing symlink
            if dst_entry.exists():
                dst_entry.unlink()
            dst_entry.symlink_to(src_entry)
