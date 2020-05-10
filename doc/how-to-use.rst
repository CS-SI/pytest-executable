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

How to use
==========

The |ptx| plugin can be used in a wide variety of ways, the following sections
explain how.


Run |exe| only
---------------------

:command:`pytest --exe-runner <path/to/runner> <path/to/tests/inputs> -k runner`

This command will execute the |exe| for all the test cases that are found in
the input tree under :file:`path/to/tests/inputs`. A test case is identified by
a directory that contains a |yaml| file. For each of the test cases found,
|ptx| will create an output directory with the same directory hierarchy and run
the cases in that output directory. By default, the root directory of the
output tree is :file:`tests-output`, this can be changed with the option
:option:`--exe-output-root`. Finally, the :option:`-k runner` option instructs
|pytest| to only execute the |runner| and nothing more, see :ref:`filter` for
more informations on doing only some of the processing.

For instance, if the tests input tree contains::

   path/to/tests/inputs
   ├── dir-1
   │   ├── input
   │   └── test_case.yaml
   └── dir-2
       ├── input
       └── test_case.yaml

Then the tests output tree is::

   tests-output
   ├── dir-1
   │   ├── input -> path/to/tests/inputs/dir-1/input
   │   ├── output
   │   ├── executable.stderr
   │   ├── executable.stdout
   │   ├── runner.sh
   │   ├── runner.sh.stderr
   │   └── runner.sh.stdout
   ├── dir-2
       ├── input -> path/to/tests/inputs/dir-2/input
       ├── output
       ├── executable.stderr
       ├── executable.stdout
       ├── runner.sh
       ├── runner.sh.stderr
       └── runner.sh.stdout

For a given test case, for instance :file:`tests-output/dir-1`,
the output directory contains:

output
   the output file produced by the execution of the |exe|, in practice there
   can be any number of output files and directories produced.

input
    a symbolic link to the file in the test input directory, in pratice
    there can be any number of input files.

executable.stderr
    contains the error messages from the |exe| execution

executable.stdout
    contains the log messages from the |exe| execution

runner.sh
    a copy of the |runner| defined with :option:`--exe-runner`, eventually
    modified by |ptx| for replacing the placeholders. Executing this script
    directly from a console shall produce the same results as when it is
    executed by |ptx|. This script is intended to be as much as possible
    independent of the execution context such that it can be executed
    independently of |ptx| in a reproductible way, i.e. it is self contained
    and does not depend on the shell context.

runner.sh.stderr
    contains the error messages from the |runner| execution

runner.sh.stdout
    contains the log messages from the |runner| execution

If you need to manually run the |exe| for a test case, for debugging
purposes for instance, just go to its output directory, for instance
:command:`cd tests-output/dir-1`, and execute the |runner|.


Do default regression checking without running executable
---------------------------------------------------------

:command:`pytest --exe-regression-root <path/to/tests/references> <path/to/tests/inputs> --exe-overwrite-output`

We assume that the |exe| results have already been produced for the test cases
considered. This is not enough though because the output directory already
exists and |ptx| will by default prevent the user from silently modifying any
existing test output directories. In that case, the option
:option:`--exe-overwrite-output` shall be used. The above command line will compare
the results in the default output tree with the references, if the existing
|exe| results are in a different directory then you need to add the path to it
with :command:`--exe-output-root`.

The option :option:`--exe-regression-root` points to the root directory with the
regression references tree . This tree shall have the same hierarchy as the
output tree but it only contains the results files that are used for doing the
regression checks.


Run |exe| and do default regression checks
-------------------------------------------------

:command:`pytest --exe-runner <path/to/runner> --exe-regression-root <path/to/tests/references> <path/to/tests/inputs>`

.. note::

   Currently this can only be used when |exe| execution is done on the same
   machine as the one that execute the regression checks, i.e. this will not
   work when |exe| is submitted through a job scheduler.

Finally, checks are done on the |exe| log files to verify that the file
:file:`executable.stdout` exists and is not empty, and that the file
:file:`executable.stderr` exists and is empty.
