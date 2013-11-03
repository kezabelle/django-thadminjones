#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def tidy_requirements(requirement_file):
    """
    simplistic parsing of our requirements files to generate dependencies for
    the setup file.
    """
    with open(requirement_file) as dependencies:
        for line in dependencies:
            line = line.strip()
            # make sure any hard pinned versions are instead treated as loose
            # minimum versions, see
            # http://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
            line = line.replace('==', '>=')
            if line and not line.startswith('#'):
                yield line


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')
requirements = set(tidy_requirements('requirements.txt'))

# if in development mode, install the requirements for the test server
if sys.argv[-1] == 'develop':
    test_requirements = set(tidy_requirements(os.path.join('test_project',
                                                           'requirements.txt')))
    requirements = requirements.union(test_requirements)

setup(
    name='django-thadminjones',
    version='0.1.0',
    description='A minimally intrusive Django admin theme',
    long_description=readme + '\n\n' + history,
    author='Keryn Knight',
    author_email='python-package@kerynknight.com',
    url='https://github.com/kezabelle/django-thadminjones/tree/0.1.0',
    packages=[
        'thadminjones',
    ],
    package_dir={'thadminjones': 'thadminjones'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='django admin theme thadminjones',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Framework :: Django',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Topic :: Internet :: WWW/HTTP',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    platforms=['OS Independent'],
    # test_suite='tests',
)
