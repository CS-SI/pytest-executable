.. _`changelog`:

Changelog
=========

All notable changes to this project will be documented here.

The format is based on `Keep a Changelog
<https://keepachangelog.com/en/1.0.0/>`_, and this project adheres to `Semantic
Versioning <https://semver.org/spec/v2.0.0.html>`_.

Unreleased
----------

Changed
~~~~~~~
- The name of the runner shell script in the output directories is the one
  passed to the CLI instead of the hardcoded one.
- All the names of the CLI options have been prefixed with :option:`--exe-` to
  prevent name clashes with other plugins options.
- It is easier to define the settings to execute the runner shell script for a
  test case thanks to a dedicated section in test-settings.yaml.
- Rename *test_case.yaml* to *test-settings.yaml*.

Added
~~~~~
- Testing on MacOS.
- :option:`--exe-test-module` cli option for setting the default test module
- Add timeout setting for the runner execution.

Removed
~~~~~~~
- The log files testing in the builtin test module.

Fixed
~~~~~
- Tests execution order when a test module is in sub-directory of the yaml
  settings.
- Marks of a test case not propagated to all test modules.

0.4.0 - 2020-05-03
------------------

Removed
~~~~~~~
- equal_nan option is too specific and can easily be added with a custom
  fixture.

0.3.1 - 2020-03-30
------------------

Added
~~~~~
- Report generation can handle a sphinx _static directory.

0.3.0 - 2020-03-19
------------------

Added
~~~~~
- How to use skip and xfail marks in the docs.
- How to use a proxy with anaconda in the docs.
- Better error message when :option:`--runner` do not get a script.

Changed
~~~~~~~
- Placeholder in the runner script are compliant with bash (use {{}} instead of
  {}).
- Report generation is done for all the tests at once and only requires a
  report generator script.

Fixed
~~~~~
- #8393: check that :option:`--clean-output` and :option:`--overwrite-output`
  are not used both.
- Output directory creation no longer fails when the input directory tree has
  one level.

Removed
~~~~~~~
- Useless :option:`--nproc` command line argument, because this can be done
  with a custom default :file:`test_case.yaml` passed to the command line
  argument :option:`--default-settings`.

0.2.1 - 2020-01-14
------------------

Fixed
~~~~~
- #7043: skip regression tests when reference files are missing, no longer
  raise error.
