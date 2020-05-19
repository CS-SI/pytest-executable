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

.. _add-test-case-label:

Add a test case
===============

A test case is composed of an input directory with:

- the input files required by the |runner|,
- a |yaml| file with the |ptx| settings,
- any optionnal |pytest| python modules for performing additionnal tests.

.. warning::

   The input directory of a test case shall not contain any of the files created by
   the execution of the |exe| or of the additional python modules, otherwise
   they may badly interfere with the executions done by |ptx|. In other words:
   do not run anything in the input directory of a test case, this directory
   shall only contain input data.

The |yaml| file is used by |ptx| for several things. When this file is
found, |ptx| will:
   
   1. create the output directory of the test case and, if needed, its parents,
   4. execute the tests defined in the default test module,
   5. execute the tests defined in the additional test modules.
   5. execute the tests defined in the parent directories.

The parents of an output directory are created such that the path from the
directory where |pytest| is executed to the input directory of the test case is
the same but for the first parent. This way, the directories hierarchy below
the first parent of both the inputs and the outputs trees are the same.

If |yaml| is empty, then the default settings are used. If
:option:`--exe-default-settings` is not set, the default settings are the
builtin ones:

 .. literalinclude:: ../src/pytest_executable/test_case.yaml

The following gives a description of the contents of |yaml|.

.. note::

   If other settings not described below exist in |yaml|, they will be ignored
   by |ptx|. This means that you can use |yaml| to store settings for other
   purposes than |ptx|.

Runner section
--------------

The purpose of this section is to be able to precisely define how to run the
|exe| for each test case. The *runner* section contains key-value pairs of
settings to be used for replacing placeholders in the |runner| passed to
:option:`--exe-runner`. For a key to be replaced, the |runner| shall contain
the key between double curly braces.

For instance, if |yaml| of a test case contains:

.. code-block:: yaml

   runner:
      nproc: 10

and the |runner| passed to :option:`--exe-runner` contains:

.. code-block:: console

   mpirun -np {{nproc}} executable

then this line in the actual |runner| used to run the test case will be:

.. code-block:: console

   mpirun -np 10 executable

.. _yaml-ref:

Reference files
---------------

The reference files are used to check for regressions on the files created by
the |exe|. Those checks can be done by comparing the files with a tolerance
, see :ref:`yaml-tol`. The *references* section shall contain a list of paths
to the files to be compared. A path shall be defined relatively to the test
case outpput directory, it may use any shell pattern like :file:`**`,
:file:`*`, :file:`?`, for instance:

.. code-block:: yaml

   references:
      - output/file
      - '**/*.txt'

Note that |ptx| does not know how to check for regression on files, you have to
implement the |pytest| tests by yourself. To get the path to the references
files in a test function, use the fixture :ref:`regression-path-fixtures`.

.. _yaml-tol:

Tolerances
----------

A tolerance is used to define how close shall be 2 data to be considered as
equal. It can be used when checking for regression by comparing files, see
:ref:`yaml-ref`. To set the tolerances for the data named *data-name1* and
*data-name2*:

.. code-block:: yaml

   tolerances:
       data-name1:
           abs: 1.
       data-name2:
           rel: 0.
           abs: 0.

For a given name, if one of the tolerance value is not defined, like the
**rel** one for the **data-name1**, then its value will be set to **0.**.

Note that |ptx| does not know how to use a tolerance, you have to implement it
by yourself in a |pytest| tests. To get the tolerance in a test function, use
the :ref:`tolerances-fixtures`.

.. _yaml-marks:

Marks
-----

A mark is a |pytest| feature that allows to select some of the tests to be
executed, see :ref:`mark_usage`. This is how to add marks to a test case, for
instance the **slow** and **big** marks:

.. code-block:: yaml

   marks:
      - slow
      - big

Such a declared mark will be set to all the test functions under a test case,
either from the default test module or from an additional |pytest| module.

You can also use the marks that already existing. In particular, the `skip` and
`xfail` marks provided by |pytest| can be used. The `skip` mark tells pytest to
record but not execute the built-in test events of a test case. The `xfail`
mark tells pytest to expect that at least one of the built-in test events will
fail.

Marks declaration
-----------------

The marks defined in all test cases shall be declared to |pytest| in order to
be used. This is done in the file :file:`pytest.ini` that shall be created in
the parent folder of the test inputs directory tree, where the |pytest| command
is executed. This file shall have the format:

.. code-block:: ini

   [pytest]
   markers =
       slow: one line explanation of what slow means
       big: one line explanation of what big means
