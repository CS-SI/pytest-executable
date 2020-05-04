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

Welcome to |ptx| documentation!
===============================

This is the user guide for |ptx|, a |pytest| plugin for checking and validating an |executable|.


Overview
--------

The |ptx| plugin allows to both automatically check |executable| results and
post-process them. In this guide, a `check` is a testing event that can be
automatically verified and can provide an OK or KO outcome, like checking that
2 numbers are equal. In contrast, a `post-process` is a testing event that
solely produces additional data, like numerical or graphical data, which has to
be analyzed manually in order to be qualified as OK or KO. The |ptx| plugin
may also generate test reports and users may add custom check and
post-processing events.

The |ptx| plugin works with several test cases directory trees for:

- the inputs
- the outputs
- the regression references

There can be more than one regression references trees for storing different
sets of references, for instance for comparing the results against more than
one version of |executable|. All the directory trees have the same hierarchy,
this convention allows |ptx| to work out what to test and what to check.
Except for the inputs tree, you do not have to manually create the directory
hierarchies, as they are automatically created by |ptx| when it is executed.

In the inputs tree, a test case is a directory that contains:

- the |executable| input files
- a |yaml| file with basic settings
- optionnal |pytest| and python scripts for adding checks and post-processes

In the outputs tree, a test case directory typically contains:

- symbolic links to the |executable| input files from the inputs tree
- a shell script to execute |executable|
- the files produced by the execution of |executable|
- eventually, the files produced by the additional post-processing

In a regression references tree, a test case directory shall contains all the
result files required for performing the checks.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   tutorial
   test-case
   post-processing
   fixtures
   test_case_yaml
   changelog


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
