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

The purpose of test fixtures is to ease the writing of test functions by
providing informations and data automatically. You may find more documentation
on |pytest| fixture in its `official documentation
<https://docs.pytest.org/en/latest/fixture.html>`_. We describe here the
fixtures defined in |ptx|. Some of them are used in the default test module,
see :ref:`builtin-test-module`.

Runner fixture
--------------

This fixture is used to execute |runner|. The :py:data:`runner` object provided
by the fixture can be executed with the :py:meth:`run` method which will return
the exit status of the script execution. The value **0** of the exit status
means a successful execution.

Output path fixture
-------------------

This fixture is used to get the absolute path to the output directory of a test
case. It provides the :py:data:`output_path` variable that holds a `Path`_
object.

.. _regression-path-fixtures:

Regression path fixture
-----------------------

This fixture is used to get the paths to the reference data of a test case, see
:ref:`yaml-ref`. If :option:`--exe-regression-root` is not used then the test
functions that use the fixture are skipped. Otherwise, the test functions that
use this fixture are called once per reference item (file or directory)
declared in the references section of |yaml|. The fixture name is
:py:data:`regression_file_path`, it's an object with the attributes:

- :py:attr:`relative`: a `Path`_ object that contains the path to a reference
  item relatively to the test case output directory.
- :py:attr:`absolute`: a `Path`_ object that contains the absolute path to a
  reference item.

You may use this fixture with the :py:data:`output_path` fixture to get the
path to the file that shall be compared to a reference file.

.. _tolerances-fixtures:

Tolerances fixture
------------------

This fixture is used to get the values of the tolerances defined in the |yaml|,
see :ref:`yaml-tol`. It provides the :py:data:`tolerances` dictionary that
binds a data name to an object that has 2 attributes:

- :py:attr:`rel`: the relative tolerance,
- :py:attr:`abs`: the absolute tolerance.
