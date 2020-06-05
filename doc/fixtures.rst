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
providing information and data automatically. You may find more documentation
on |pytest| fixture in its `official documentation
<https://docs.pytest.org/en/latest/fixture.html>`_. We describe here the
fixtures defined in |ptx|. Some of them are used in the default test module,
see :ref:`builtin-test-module`.

.. _fixture-runner:

Runner fixture
--------------

The :py:data:`runner` fixture is used to execute the |runner| passed with
:option:`--exe-runner`. This fixture is an :py:class:`object
<pytest_executable.script_runner.ScriptRunner>` which can execute the script
with the :py:meth:`run` method. This method returns the exit status of the
script execution. The value of the exit status shall be **0** when the
execution is successful.

When :option:`--exe-runner` is not set, a function that uses this fixture will
be skipped.

.. _fixture-output_path:

Output path fixture
-------------------

The :py:data:`output_path` fixture provides the absolute path to the output
directory of a test case as a `Path`_ object.

.. _regression-path-fixtures:

Regression path fixture
-----------------------

The :py:data:`regression_file_path` fixture provides the paths to the reference
data of a test case. A test function that use this fixture is called once per
reference item (file or directory) declared in the :ref:`yaml-ref` of a |yaml|
(thanks to the `parametrize
<https://docs.pytest.org/en/latest/parametrize.html>`_ feature). The
:py:data:`regression_file_path` object has the attributes:

- :py:attr:`relative`: a `Path`_ object that contains the path to a reference
  item relatively to the output directory of the test case.
- :py:attr:`absolute`: a `Path`_ object that contains the absolute path to a
  reference item.

If :option:`--exe-regression-root` is not set then a test function that uses
the fixture is skipped.

You may use this fixture with the :ref:`fixture-output_path` to get the path to
an output file that shall be compared to a reference file.

For instance, if a |yaml| under :file:`inputs/case` contains:

.. code-block:: yaml

   references:
      - output/file
      - '**/*.txt'

and if :option:`--exe-regression-root` is set to a directory :file:`references`
that contains:

.. code-block:: text

   references
   └── case
       ├── 0.txt
       └── output
           ├── a.txt
           └── file

then a test function that uses the fixture will be called once per item of the
following list:

.. code-block:: py

   [
     "references/case/output/file",
     "references/case/0.txt",
     "references/case/output/a.txt",
   ]

and for each these items, the :py:data:`regression_file_path` is set as
described above with the relative and absolute paths.

.. _tolerances-fixtures:

Tolerances fixture
------------------

The :py:data:`tolerances` fixture provides the contents of the :ref:`yaml-tol`
of a |yaml| as a dictionary that maps names to :py:class:`Tolerances
<pytest_executable.settings.Tolerances>` objects.

For instance, if a |yaml| contains:

.. code-block:: yaml

   tolerances:
       data-name1:
           abs: 1.
       data-name2:
           rel: 0.
           abs: 0.

then the fixture object is such that:

.. code-block:: py

   tolerances["data-name1"].abs = 1.
   tolerances["data-name1"].rel = 0.
   tolerances["data-name2"].abs = 0.
   tolerances["data-name2"].rel = 0.
