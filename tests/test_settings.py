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
"""Tests for the settings container."""
from __future__ import annotations

import pytest
from jsonschema import ValidationError
from pytest_executable.plugin import SETTINGS_PATH as DEFAULT_SETTINGS_FILE
from pytest_executable.settings import Settings
from pytest_executable.settings import Tolerances


@pytest.fixture
def default_settings():
    """Fixture that returns a hand made default Settings object."""
    return Settings(runner={}, marks=set(), references=set(), tolerances={})


def _test_merge(tmp_path, yaml_str, ref_settings):
    # helper function
    settings_file = tmp_path / "settings.yaml"
    settings_file.write_text(yaml_str)
    assert (
        Settings.from_local_file(DEFAULT_SETTINGS_FILE, settings_file) == ref_settings
    )


def test_defaults(tmp_path, default_settings):
    """Test yaml merge with default settings."""
    # default settings merged with itself
    yaml_str = ""
    _test_merge(tmp_path, yaml_str, default_settings)


def test_merge(tmp_path):
    """Test yaml merge with default settings."""
    # default settings merged with itself
    yaml_str = ""
    ref_settings = Settings.from_local_file(
        DEFAULT_SETTINGS_FILE, DEFAULT_SETTINGS_FILE
    )
    _test_merge(tmp_path, yaml_str, ref_settings)


def test_merge_0(tmp_path, default_settings):
    """Test merge existing dict item."""
    yaml_str = """
tolerances:
    Velocity:
        rel: 1.
    """
    default_settings.tolerances["Velocity"] = Tolerances()
    default_settings.tolerances["Velocity"].rel = 1
    _test_merge(tmp_path, yaml_str, default_settings)


def test_merge_1(tmp_path, default_settings):
    """Test merge new dict item."""
    yaml_str = """
tolerances:
    X:
        rel: 1.
    """
    default_settings.tolerances["X"] = Tolerances(rel=1.0, abs=0.0)
    _test_merge(tmp_path, yaml_str, default_settings)


def test_merge_2(tmp_path, default_settings):
    """Test merge new dict item."""
    yaml_str = """
marks:
    - mark
    """
    default_settings.marks = {"mark"}
    _test_merge(tmp_path, yaml_str, default_settings)


@pytest.mark.parametrize(
    "yaml_str",
    (  # marks shall be unique
        """
marks:
    - x
    - x
        """,
        # references shall be unique
        """
references:
    - x
    - x
        """,
        # runner shall be an object
        """
runner: 0
        """,
        """
runner: []
        """,
        # tolerances shall be rel or abs
        """
tolerances:
    quantity:
        X: 1.
        """,
        # rel shall be number
        """
tolerances:
    quantity:
        rel: x
        """,
        # rel shall be positive
        """
tolerances:
    quantity:
        rel: -1.
        """,
    ),
)
def test_yaml_validation(tmp_path, yaml_str):
    """Test yaml schema validation."""
    settings_file = tmp_path / "settings.yaml"
    settings_file.write_text(yaml_str)
    with pytest.raises(ValidationError):
        Settings.from_local_file(DEFAULT_SETTINGS_FILE, settings_file)


def test_alien_item(tmp_path, default_settings):
    """Test that an alien item in the yaml is ignored."""
    yaml_str = "dummy: ''"
    settings_file = tmp_path / "settings.yaml"
    settings_file.write_text(yaml_str)
    settings = Settings.from_local_file(DEFAULT_SETTINGS_FILE, settings_file)
    assert settings == default_settings
