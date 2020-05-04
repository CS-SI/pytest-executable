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

A test case is composed of a directory with:

- the |executable| input files
- a |yaml| file with basic settings
- optionnal |pytest| and python module for adding checks and post-processes

The |executable| input files shall use the naming convention :file:`case.labs`
and :file:`case.pbd`. Among the optionnal modules, there shall be at least one
that is discoverable by |pytest|, i.e. a python module which name starts with
:file:`test_` and which contains at least one function which also starts with
**test_**.

.. note::

   A test case directory shall not contain any of the files created by the
   execution of |executable| or of the processing defined in the python modules,
   otherwise they may badly interfere with the execution of the testing tool.
   In other words, do not run anything in the input directory.

The |yaml| file is used by |ptx| for several things. When this file is
found, |ptx| will create the test case output directory, then identify the
settings for running the case and finally perform the checks and
post-porcesses. If |yaml| is empty, then the default settings are used, which
is equivalent to using a |yaml| with the following contents:

 .. literalinclude:: ../src/pytest_executable/test_case.yaml

This file is in yaml format, a widely used human friendly file format that
allows to define nested sections, lists of items, key-value pairs and more. To
change a default settings, just define it in the |yaml| as explaned in the
following sections.


Number of parallel processes
----------------------------

To change the number of parallel processes:

.. code-block:: yaml

   nproc: 10


Regression reference files
--------------------------

Reference files are used to do regression checks on the files produced by
|executable|. The regression is
done by comparing the files with a given tolerance (explained in the next
section). The `references` setting shall contain a list of paths to the files
to be compared. A path shall be defined relatively to the test case directory,
it may use any shell pattern like :file:`**`, :file:`*`, :file:`?`, for
instance:

.. code-block:: yaml

   references:
      - path/to/file/relative/to/test/case


Tolerances
----------

To change the tolerance for comparing the Velocity variable and allow to
compare a new NewVariable variable:

.. code-block:: yaml

   tolerances:
       Velocity:
           abs: 1.
       NewVariable:
           rel: 0.
           abs: 0.

If one of the tolerance value is not defined, like the **abs** one for the
**Velocity**, then its value will be set to **0.**.


Marks
-----

A mark is a |pytest| feature that allows to select some of the tests to be
executed. A mark is a kind of tag or label assigned to a test. This is how to
add marks to a test case, for instance the **slow** and **isotropy** marks:

.. code-block:: yaml

   marks:
      - slow
      - isotropy

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
       slow: one line explanation of slow
       isotropy: one line explanation of isotropy
