# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Required packages for install, test, docs, and tests."""

import os
import re

from setuptools import setup, find_packages


install_requires = [
    'appdirs>=1.4.4',
    'flowserv-core>=0.9.0',
    'refdata>=0.2.0',
    'openclean-core>=0.4.1'
]


tests_require = [
    'coverage>=4.0',
    'pytest',
    'pytest-cov',
    'tox',
    'docker'
]


docs_require = [
    'Sphinx',
    'sphinx-rtd-theme',
    'sphinxcontrib-apidoc'
]


extras_require = {
    'docs': docs_require,
    'tests': tests_require,
    'dev': tests_require + docs_require
}


# Get the version string from the version.py file in the openclean_metanome
# package. Based on:
# https://stackoverflow.com/questions/458550
with open(os.path.join('openclean_metanome', 'version.py'), 'rt') as f:
    filecontent = f.read()
match = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", filecontent, re.M)
if match is not None:
    version = match.group(1)
else:
    raise RuntimeError('unable to find version string in %s.' % (filecontent,))


# Get long project description text from the README.rst file
with open('README.rst', 'rt') as f:
    readme = f.read()


setup(
    name='openclean-metanome',
    version=version,
    description='openclean Metanome Python Package',
    long_description=readme,
    long_description_content_type='text/x-rst',
    keywords='data cleaning',
    url='https://github.com/VIDA-NYU/openclean-metanome',
    author='Heiko Mueller',
    author_email='heiko.muller@gmail.com',
    license_file='LICENSE',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    extras_require=extras_require,
    tests_require=tests_require,
    install_requires=install_requires,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python'
    ]
)
