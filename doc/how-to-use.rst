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

Overview
========

Directory trees
---------------

The |ptx| plugin deals with multiple directory trees:

- the inputs
- the outputs
- the regression references

The inputs tree contains the files required to run an |exe| and to check its
outcomes for different settings. It is composed of test cases as directories at
the leaves of the tree. To create a test case, see :ref:`add-test-case-label`.

All the directory trees have the same hierarchy, this convention allows |ptx|
to work out what to test and what to check. The outputs tree is automatically
created by |ptx|, inside it, a test case directory typically contains:

- symbolic links to the |exe| input files for the corresponding test case in
  the inputs tree
- a |runner| to execute |exe|
- the files produced by the execution of |exe|
- eventually, the files produced by the additional test modules

At the beginning, a regression reference tree is generally created from an
existing outputs tree. In a regression references tree, a test case directory
shall contain all the result files required for performing the comparisons for
the regression testing. There can be more than one regression references trees
for storing different sets of references, for instance for comparing the
results against more than one version of |exe|.

Execution order
---------------

The |ptx| plugin will reorder the execution such that the |pytest| tests are
executed in the following order:

1. in a test case, the tests defined in the default test module (see
   :option:`--exe-test-module`),
2. any other tests defined in a test case directory, with |pytest| natural
   order,
3. any other tests defined in the parent directories of a test case.

The purposes of this order is to make sure that the |runner| and the other
default tests are executed first before the tests in other modules can be
performed on the outcome of the |exe|. It also allows to create test modules in
the parent directory of several test cases to gather their outcomes.

How to use
==========

Run the |exe| only
------------------

:command:`pytest <path/to/tests/inputs> --exe-runner <path/to/runner> -k runner`

This command will execute the |exe| for all the test cases that are found in
the input tree under :file:`path/to/tests/inputs`. A test case is identified by
a directory that contains a |yaml| file. For each of the test cases found,
|ptx| will create an output directory with the same directory hierarchy and run
the cases in that output directory. By default, the root directory of the
output tree is :file:`tests-output`, this can be changed with the option
:option:`--exe-output-root`. Finally, the :option:`-k runner` option instructs
|pytest| to only execute the |runner| and nothing more, see :ref:`filter` for
more information on doing only some of the processing.

For instance, if the tests input tree contains::

   path/to/tests/inputs
   ├── case-1
   │   ├── input
   │   └── test-settings.yaml
   └── case-2
       ├── input
       └── test-settings.yaml

Then the tests output tree is::

   tests-output
   ├── case-1
   │   ├── input -> path/to/tests/inputs/case-1/input
   │   ├── output
   │   ├── executable.stderr
   │   ├── executable.stdout
   │   ├── runner.sh
   │   ├── runner.sh.stderr
   │   └── runner.sh.stdout
   └── case-2
       ├── input -> path/to/tests/inputs/case-2/input
       ├── output
       ├── executable.stderr
       ├── executable.stdout
       ├── runner.sh
       ├── runner.sh.stderr
       └── runner.sh.stdout

For a given test case, for instance :file:`tests-output/case-1`,
the output directory contains:

output
   the output file produced by the execution of the |exe|, in practice there
   can be any number of output files and directories produced.

input
    a symbolic link to the file in the test input directory, in practice
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
    independently of |ptx| in a reproducible way, i.e. it is self contained
    and does not depend on the shell context.

runner.sh.stderr
    contains the error messages from the |runner| execution

runner.sh.stdout
    contains the log messages from the |runner| execution

If you need to manually run the |exe| for a test case, for debugging
purposes for instance, just go to its output directory, for instance
:command:`cd tests-output/case-1`, and execute the |runner|.


Check regressions without running the |exe|
-------------------------------------------

:command:`pytest <path/to/tests/inputs> --exe-regression-root <path/to/tests/references> --exe-overwrite-output`

We assume that the |exe| results have already been produced for the test cases
considered. This is not enough though because the output directory already
exists and |ptx| will by default prevent the user from silently modifying any
existing test output directories. In that case, the option
:option:`--exe-overwrite-output` shall be used. The above command line will
compare the results in the default output tree with the references, if the
existing |exe| results are in a different directory then you need to add the
path to it with :option:`--exe-output-root`.

The option :option:`--exe-regression-root` points to the root directory with
the regression references tree . This tree shall have the same hierarchy as the
output tree but it only contains the results files that are used for doing the
regression checks.


Run the |exe| and do default regression checks
----------------------------------------------

:command:`pytest <path/to/tests/inputs> --exe-runner <path/to/runner> --exe-regression-root <path/to/tests/references>`

.. note::

   Currently this can only be used when the |exe| execution is done on the same
   machine as the one that execute the regression checks, i.e. this will not
   work when the |exe| is executed on another machine.

Finally, checks are done on the |exe| log files to verify that the file
:file:`executable.stdout` exists and is not empty, and that the file
:file:`executable.stderr` exists and is empty.
