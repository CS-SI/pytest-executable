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

Installation
============

Requirements
------------

Anaconda or miniconda version 2019.07 or above is required, it can be
downloaded from anaconda.com. Once anaconda is installed (see `here
<https://docs.conda.io/projects/conda/en/latest/user-guide/configuration/use-condarc.html#config-proxy>`_
if you need to define a proxy), create the anaconda environment with

.. code-block:: console

   make environment

Now activate the anaconda environment with

.. code-block:: console

   conda activate test-tools

The remaining of this guide assumes you are in that environment. When you are
done with |ptx| and wish to leave the environment, execute

.. code-block:: console

   conda deactivate


Installation
------------

Install for development
~~~~~~~~~~~~~~~~~~~~~~~

Install for development if you intend to modify |ptx| and have your
modifications usable in the environment, i.e. without having to to do a
reinstallation after a modification. To do so run

.. code-block:: console

   make develop

You may also use this command to update an existing anaconda environment, for
instance after updating your local git clone or if you add packages dependencies.


Install for usage only
~~~~~~~~~~~~~~~~~~~~~~

If you only need to use |ptx| without having to modify it, run

.. code-block:: console

   make install

You may also use this command to update an existing anaconda environment, for
instance after updating your local git clone or if you add packages dependencies.


Documentation
-------------

To generate the documentation, run

.. code-block:: console

   make doc

Then open :file:`doc/build/html/index.html` from a web browser.


Testing the tool
----------------

The tests can be run with

.. code-block:: console

   make test

You shall run them when you modify or update |ptx|. All the tests shall be
OK, otherwise you shall not use |ptx| and contact the support team.
