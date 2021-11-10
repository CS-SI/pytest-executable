Pytest-executable
=================

.. inclusion-marker-do-not-remove

.. image:: https://img.shields.io/pypi/l/pytest-executable.svg
    :target: `quick summary`_

.. image:: https://img.shields.io/pypi/v/pytest-executable.svg
    :target: https://pypi.org/project/pytest-executable

.. image:: https://img.shields.io/conda/vn/conda-forge/pytest-executable
    :target: https://anaconda.org/conda-forge/pytest-executable

.. image:: https://img.shields.io/pypi/pyversions/pytest-executable.svg

.. image:: https://img.shields.io/badge/platform-linux%20%7C%20macos-lightgrey

.. image:: https://img.shields.io/readthedocs/pytest-executable/stable
    :target: https://pytest-executable.readthedocs.io/en/stable/?badge=stable
    :alt: Read The Docs Status

.. image:: https://img.shields.io/travis/CS-SI/pytest-executable/master
    :target: https://travis-ci.org/CS-SI/pytest-executable
    :alt: Travis-CI Build Status

.. image:: https://img.shields.io/codecov/c/gh/CS-SI/pytest-executable/develop
    :target: https://codecov.io/gh/CS-SI/pytest-executable
    :alt: Codecov coverage report

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

*pytest-executable* is a `pytest`_ plugin for simplifying the black-box
testing of an executable, be it written in python or not. It helps to avoid
writing the boilerplate test code to:

- define the settings of a test case in a yaml file,
- spawn a subprocess for running an executable,
- reorder the tests properly either for a single test case or across several test cases,
- handle the outputs and references directory trees,
- provide convenient fixtures to customize the checking of the outcome of an executable.

It integrates naturally with standard test scripts written for pytest.

This plugin is originally intended for testing executables that create
scientific data but it may hopefully be helpful for other kinds of executables.
This project is still young, but already used in a professional environment.


Documentation
-------------

The project documentation and installation instructions are available `online`_.


Contributing
------------

A contributing guide will be soon available (just a matter of free time).

Please fill an issue on the `Github issue tracker`_ for any bug report, feature
request or question.


Authors
-------

-  `Antoine Dechaume`_ - *Project creator and maintainer*


Copyright and License
---------------------

Copyright 2020, `CS GROUP`_

*pytest-executable* is a free and open source software, distributed under the
Apache License 2.0. See the `LICENSE.txt`_ file for more information, or the
`quick summary`_ of this license on `tl;drLegal`_ website.


.. _conda: https://docs.conda.io
.. _pip: https://pip-installer.org
.. _pytest: https://docs.pytest.org
.. _online: https://pytest-executable.readthedocs.io
.. _Github issue tracker: https://github.com/CS-SI/pytest-executable/issues
.. _Antoine Dechaume: https://github.com/AntoineD
.. _CS GROUP: http://www.csgroup.eu
.. _`LICENSE.txt`: LICENSE.txt
.. _quick summary: https://tldrlegal.com/license/apache-license-2.0-(apache-2.0)
.. _tl;drLegal: https://tldrlegal.com
