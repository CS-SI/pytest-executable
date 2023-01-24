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
"""Provide a yaml file loader."""
from __future__ import annotations

from pathlib import Path
from typing import Any
from typing import Dict
from typing import TextIO

import jsonschema
import yaml

# basic type for the content of a yaml with a mapping at the root level
DataType = Dict[str, Any]


class YamlHelper:
    """Yaml file helper class.

    Can load and validate a yaml file, can also merge tha data 2 yaml files.

    Args:
        schema_path: Path to a schema file used for validating a yaml.
    """

    def __init__(self, schema_path: Path):
        with schema_path.open() as file_:
            self.__schema = yaml.safe_load(file_)

    def load(self, path: Path) -> DataType:
        """Return the validated data from a yaml file.

        Args:
            path: Path to a yaml file.

        Returns:
            The validated data.
        """
        data: DataType
        with path.open() as file_:
            data = yaml.safe_load(file_)

        if data is None:
            data = {}

        jsonschema.validate(data, self.__schema)

        return data

    def dump(self, data: DataType, stream: TextIO) -> None:
        """Validate and dump data to a yaml file.

        Args:
            data: Data to be dumped.
            stream: IO stream to be written to.
        """
        jsonschema.validate(data, self.__schema)
        yaml.safe_dump(data, stream)

    def load_merge(self, ref: Path, new: Path) -> DataType:
        """Merge the data of 2 yaml files.

        Args:
            ref: Path to the file to be updated with new.
            new: Path to the file to be merged into ref.

        Return:
            The merged dictionary.
        """
        return self.__recursive_update(self.load(ref), self.load(new))

    @classmethod
    def __recursive_update(cls, ref: DataType, new: DataType) -> DataType:
        """Merge recursively 2 dictionaries.

        The lists are concatenated.
        """
        for key, value in new.items():
            if isinstance(value, dict):
                ref[key] = cls.__recursive_update(ref.get(key, {}), value)
            elif isinstance(value, list):
                # append the items that were not already in the list
                for val in value:
                    if val not in ref[key]:
                        ref[key] += [val]
            else:
                ref[key] = value
        return ref
