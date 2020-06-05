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

Add a post-processing
=====================

This section show how to a add post-processing that will be run by |ptx|.


Pytest functions
----------------

In a test case input directory, create a python module with a name starting
by :file:`test_`. Then in that module, create |pytest| functions with a name
starting by :data:`test_`. Those functions will be executed and |pytest| will
catch the :py:data:`assert` statements to determine if the processing done by a
function is considered as **passed** or **failed**. The outcome of a function
could also be  **skipped** if for some reason no assertion could be evaluated.
If an exception is raised in a function, the function execution will be
considered as **failed**.

The functions are executed is a defined order: first by the test directory
name, then by the module name and finally by the function name. The sorting is
done by alphabetical order. There are 2 exceptions to this behavior:

   - the |yaml| file is always processes before all other modules in a given
     directory
   - a module in a parent directory is always run after the modules in the
     children directories, this allows for gathering the results from the
     children directories

The |pytest| functions shall take advantages of the fixtures for automatically
retrieved data from the execution context, such as the information stored in
the |yaml| or the path to the current output directory.

See :ref:`fixtures` for more information on fixtures.

See :ref:`builtin-test-module` for |pytest| function examples.


Best practices
--------------

Script naming
~~~~~~~~~~~~~

If a post-processing script has the same name in different test case
directories then each of those directories shall have a :file:`__init__.py`
file so |pytest| can use them.


External python module
~~~~~~~~~~~~~~~~~~~~~~

If you import an external python module in a |pytest| function, you shall use
the following code snippet to prevent |pytest| from failing if the module is
not available.

.. code-block:: python

    pytest.importorskip('external_module',
                        reason='skip test because external_module cannot be imported')
    from external_module import a_function, a_class

If the external module is installed in an environment not compatible with the
anaconda environment of |ptx|, then execute the module through a `subprocess
<https://docs.python.org/3.7/library/subprocess.html#using-the-subprocess-module>`_
call. For instance:

.. code-block:: python

    import subprocess
    command = 'python external_module.py'
    subprocess.run(command.split())
