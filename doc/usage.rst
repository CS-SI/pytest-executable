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

.. _Sphinx: https://www.sphinx-doc.org


Installation
============

Install using `pip <http://pip-installer.org/>`_:

.. code-block:: console

    pip install pytest-executable


Command line interface
======================

The |pytest| command line shall be executed from the directory that contains the inputs
root directory.


Plugin options
--------------

.. option:: --exe-runner PATH

    use the shell script at PATH to run the |exe|, if omitted then the |exe| is
    not run.

    This shell script may contain placeholders, such as `{{nproc}}` and
    `{{output_path}}`. The placeholders will be replaced with the parameters
    determined from the context (either a pytest cli option or a setting
    defined in a test case via the :ref:`test_case.yaml
    <add-test-case-label>`), and a final |runner| is saved for each test cases
    to be run in their output directories. This latter is used to run the
    |exe|.

    A typical script for running the |exe| with MPI could be:

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

   use PATH as the yaml file with the global default test settings instead of
   the built-in ones

.. option:: --exe-report-generator PATH

   use PATH as the script to generate the test report

   See the :file:`report-conf` directory for an example of such a script.

   .. note::

      The report generator script may require to install additionnal
      dependencies, such as sphinx, which are not required by the plugin.


.. _filter:

Standard pytest options
-----------------------

You can get all the standard command line options of |pytest| by executing
:command:`pytest -h`. In particular, to run only some of the test cases in the
inputs tree, or to execute only some of the test functions, you may use one of
the following ways:

Use multiple path patterns
   Instead of providing the path to the root of the inputs tree, you may
   provide the path to one or more of its sub-directories, for instance:

   :command:`pytest --exe-runner <path/to/runner> <path/to/tests/inputs/sub-directory1> <path/to/tests/inputs/sub/sub/sub-directory2>`

   You may also use shell patterns (with `*` and `?` characters) in the paths like:

   :command:`pytest --exe-runner <path/to/runner> <path/to/tests/inputs/*/sub-directory?>`

Use marks
   A test case could be assigned one or more marks in the |yaml| file, then
   with :option:`-m` only the test cases that match a given mark expression
   will be run. A mark expression is a logical expression that combines marks
   and yields a truth value. For example, to run only the tests that have the
   mark1 mark but not the mark2 mark, use :option:`-m "mark1 and not mark2"`.
   The logical operator `or` could be used as well.

Use substring expression
   Like the marks, any part (substring) of the name of a test case or of a test
   function can be used to filter what will be executed. For instance to only
   execute the tests that have the string `transition` anywhere in their name,
   use :option:`-k "transition"`. Or, to execute only the functions that have
   `runner` in their names, use :option:`-k "runner"`. Logical expressions
   could be used to combine more susbtrings as well.

Process last failed tests only
   To only execute the tests that previously failed, use
   :option:`--last-failed`.

Show the markers
   Use :option:`--markers` to show the available markers without executing the
   tests.

Show the tests to be executed
   Use :option:`--collect-only` to show the test cases and the test events
   (functions) selected without executing them. You may combine this option
   with other options, like the one above to filter the test cases.
