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
"""Test for the plugin itself."""
from __future__ import annotations

import inspect


def assert_outcomes(result, **kwargs):
    """Wrap result.assert_outcomes different API vs pytest versions."""
    signature_params = inspect.signature(result.assert_outcomes).parameters
    if "errors" not in signature_params and "errors" in kwargs:
        kwargs["error"] = kwargs.pop("errors")
    result.assert_outcomes(**kwargs)
