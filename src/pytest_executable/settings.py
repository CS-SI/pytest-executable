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
"""Provides the container for the settings of a test case.

We use a dataclass because a dictionary does not offer easy checking and code completion.
"""
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import fields
from pathlib import Path

from .yaml_helper import YamlHelper

# the yaml file with the default settings is in the same directory as the
# current module, the yaml schema too
SETTINGS_SCHEMA_FILE = Path(__file__).parent / "test-settings-schema.yaml"


@dataclass
class Tolerances:
    """Comparison tolerances.

    Attributes:
        rel: The relative tolerance.
        abs: The absolute tolerance.
    """

    rel: float = 0.0
    abs: float = 0.0


@dataclass
class Settings:
    """Test settings container.

    This contains the test settings read from a yaml file.

    Attributes:
        runner: The settings for the script runner.
        marks: The pytest marks.
        references: The reference files path patterns.
        tolerances: The comparison tolerances.
    """

    runner: dict[str, str]
    marks: set[str]
    references: set[str]
    tolerances: dict[str, Tolerances]

    def __post_init__(self) -> None:
        """Coerce the attributes types."""
        self.marks = set(self.marks)
        self.references = set(self.references)
        for key, value in self.tolerances.copy().items():
            self.tolerances[key] = Tolerances(**value)  # type:ignore

    @classmethod
    def from_local_file(cls, path_global: Path, path_local: Path) -> Settings:
        """Create a :class:`Settings` object from 2 yaml files.

        The contents of the local file overrides or extends the contents of the
        global one. The items that have no corresponding attributes in the
        current class are ignored.

        Args:
            path_global: Path to a yaml file with global settings.
            path_local: Path to a yaml file with local settings.

        Returns:
            Settings object.
        """
        loader = YamlHelper(SETTINGS_SCHEMA_FILE)
        # contains the settings and eventually additional items
        loaded_settings = loader.load_merge(path_global, path_local)
        # keep the used settings
        settings = {}
        for field in fields(cls):
            name = field.name
            settings[name] = loaded_settings[name]
        return cls(**settings)
