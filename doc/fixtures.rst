.. Copyright 2020 CS Systemes d'Information, http://www.c-s.fr
..
.. This file is part of pytest-executable
..     https://www.github.com/CS-SI/pytest-executable
..
.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
..     http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.

.. _Path: https://docs.python.org/3/library/pathlib.html#basic-use
.. _Sphinx: https://www.sphinx-doc.org

.. _fixtures:

Fixtures
========

The purpose of the test fixtures is to ease the writing of test functions by
providing informations and data automatically. You may find more documentation
on |pytest| fixture in its `official documentation
<https://docs.pytest.org/en/latest/fixture.html>`_. We describe here the
fixtures defined in |ptx|. Some of them are used in the default test module,
see :ref:`builtin-test-module`.

Runner fixture
--------------

The :py:data:`runner` fixture is used to execute the |runner|. It will create
the runner script in the output directory of a test case from the script passed
to the pytest command line with the option :option:`--exe-runner`. The
placeholders in the script are replaced with their actual values determined
from the settings in the yaml file and the output path. The runner object
passed by the fixture can be executed with the :py:meth:`run` method which will
return the exit status of the script execution. The value of the exit status
shall be **0** when the execution is successful.

When the runner script is not passed to :option:`--exe-runner`, a function that
uses this fixture will be skipped.

Output path fixture
-------------------

The :py:data:`output_path` fixture provides the absolute path to the output
directory of a test case as a `Path`_ object.

.. _regression-path-fixtures:

Regression path fixture
-----------------------

The :py:data:`regression_file_path` fixture provides the paths to the reference
data of a test case, see :ref:`yaml-ref`. If :option:`--exe-regression-root` is
not set then a test function that uses the fixture is skipped. Otherwise, a
test function that use this fixture is called once per reference item (file or
directory) declared in the references section of |yaml| (thanks to the
`parametrize <https://docs.pytest.org/en/latest/parametrize.html>`_). The
:py:data:`regression_file_path` object has the attributes:

- :py:attr:`relative`: a `Path`_ object that contains the path to a reference
  item relatively to the output directory of the test case.
- :py:attr:`absolute`: a `Path`_ object that contains the absolute path to a
  reference item.

You may use this fixture with the :py:data:`output_path` fixture to get the
path to the file that shall be compared to a reference file.

.. _tolerances-fixtures:

Tolerances fixture
------------------

The :py:data:`tolerances` fixture provides the tolerances defined in the
|yaml|, see :ref:`yaml-tol`. The :py:data:`tolerances` object is a dictionary
that binds a data name to an object that has 2 attributes:

- :py:attr:`rel`: the relative tolerance,
- :py:attr:`abs`: the absolute tolerance.
