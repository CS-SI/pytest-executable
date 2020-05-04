"""Entry point to python packaging.

See https://python-packaging-user-guide.readthedocs.io for more details.
See setup.cfg for other settings.
"""

import setuptools

import versioneer

setuptools.setup(
    version=versioneer.get_version(), cmdclass=versioneer.get_cmdclass(),
)
