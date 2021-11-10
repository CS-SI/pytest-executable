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

.. _conda: https://docs.conda.io
.. _pip: https://pip.pypa.io/en/stable/installing
.. _report-conf: https://github.com/CS-SI/pytest-executable/tree/master/report-conf


Installation
============

Install using `pip`_:

.. code-block:: console

    pip install pytest-executable

Install using `conda`_:

.. code-block:: console

    conda install pytest-executable -c conda-forge


Command line interface
======================

The |pytest| command line shall be executed from the directory that contains
the inputs root directory.


Plugin options
--------------

.. option:: --exe-runner PATH

    use the shell script at PATH to run the |exe|.

    This shell script may contain placeholders, such as *{{output_path}}* or
    others defined in the :ref:`yaml-runner` of a |yaml|. A final |runner|,
    with replaced placeholders, is written in the output directory of a test
    case (*{{output_path}}* is set to this path). This final script is then
    executed before any other test functions of a test case. See
    :ref:`fixture-runner` for further information.

    If this option is not defined then the |runner| will not be executed, but
    all the other test functions will.

    A typical |runner| for running the |exe| with MPI could be:

    .. literalinclude:: ../mpi_runner.sh
      :language: bash

.. option:: --exe-output-root PATH

   use PATH as the root for the output directory tree, default: tests-output

.. option:: --exe-overwrite-output

   overwrite existing files in the output directories

.. option:: --exe-clean-output

   clean the output directories before executing the tests

.. option:: --exe-regression-root PATH

   use PATH as the root directory with the references for the regression
   testing, if omitted then the tests using the regression_path fixture will be
   skipped

.. option:: --exe-default-settings PATH

   use PATH as the yaml file with the default test settings instead of the
   built-in ones

.. option:: --exe-test-module PATH

   use PATH as the default test module instead of the built-in one

.. option:: --exe-report-generator PATH

   use PATH as the script to generate the test report

   See :file:`generate_report.py` in the `report-conf`_ directory for an
   example of such a script.

   .. note::

      The report generator script may require to install additional
      dependencies, such as sphinx, which are not install by the |ptx| plugin.


.. _filter:

Standard pytest options
-----------------------

You can get all the standard command line options of |pytest| by executing
:command:`pytest -h`. In particular, to run only some of the test cases in the
inputs tree, or to execute only some of the test functions, you may use one of
the following ways:

Use multiple path patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~

Instead of providing the path to the root of the inputs tree, you may
provide the path to one or more of its sub-directories, for instance:

:command:`pytest --exe-runner <path/to/runner> <path/to/tests/inputs/sub-directory1> <path/to/tests/inputs/sub/sub/sub-directory2>`

You may also use shell patterns (with ``*`` and ``?`` characters) in the paths
like:

:command:`pytest --exe-runner <path/to/runner> <path/to/tests/inputs/*/sub-directory?>`

.. _mark_usage:

Use marks
~~~~~~~~~

A test case could be assigned one or more marks in the |yaml| file, see
:ref:`yaml-marks`. Use the :option:`-m` to execute only the test cases that
match a given mark expression. A mark expression is a logical expression that
combines marks and yields a truth value. For example, to run only the tests
that have the mark1 mark but not the mark2 mark, use :option:`-m "mark1 and not
mark2"`. The logical operator ``or`` could be used as well.

Use sub-string expression
~~~~~~~~~~~~~~~~~~~~~~~~~

Like the marks, any part (sub-string) of the name of a test case or of a test
function can be used to filter what will be executed. For instance to only
execute the tests that have the string ``transition`` anywhere in their name, use
:option:`-k "transition"`. Or, to execute only the functions that have ``runner``
in their names, use :option:`-k "runner"`. Logical expressions could be used to
combine more sub-strings as well.

Process last failed tests only
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To only execute the tests that previously failed, use :option:`--last-failed`.

Show the markers
~~~~~~~~~~~~~~~~

Use :option:`--markers` to show the available markers without executing the
tests.

Show the tests to be executed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use :option:`--collect-only` to show the test cases and the test events
(functions) selected without executing them. You may combine this option with
other options, like the one above to filter the test cases.
