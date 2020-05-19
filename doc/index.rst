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

This is the user guide for |ptx|, a |pytest| plugin for black-box testing an |exe|.

Overview
--------

The |ptx| plugin allows to both automatically check |exe| results and
post-process them.

The |ptx| plugin deals with multiple directory trees:

- the inputs
- the outputs
- the regression references

There can be more than one regression references trees for storing different
sets of references, for instance for comparing the results against more than
one version of |exe|. All the directory trees have the same hierarchy,
this convention allows |ptx| to work out what to test and what to check.
Except for the inputs tree, you do not have to manually create the directory
hierarchies, as they are automatically created by |ptx|.

To create a test case, see :ref:`add-test-case-label`.

In the outputs tree, a test case directory typically contains:

- symbolic links to the |exe| input files from the inputs tree
- a shell script to execute |exe|
- the files produced by the execution of |exe|
- eventually, the files produced by the additional post-processing

In a regression references tree, a test case directory shall contain all the
result files required for performing the checks.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   how-to-use
   test-case
   post-processing
   fixtures
   test_executable
   changelog


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
