#!/usr/bin/env python

"""
distutils setup (setup.py).

This is just boilerplate code, since we do like to try to keep data separate
from code as much as possible. The customizable information really comes
from file __pkginfo__.py.
"""

# Get the package information used in setup().
from __pkginfo__ import \
    author,           author_email,       classifiers,                    \
    install_requires, license,            long_description,               \
    modname,          namespace_packages, packages,         py_modules,   \
    short_desc,       version,            web,              zip_safe

__import__('pkg_resources')
from setuptools import setup

setup(
       author             = author,
       author_email       = author_email,
       classifiers        = classifiers,
       data_files=[('trepan/processor/command/help',
                    ['trepan/processor/command/help/command.rst',
                     'trepan/processor/command/help/examples.rst',
                     'trepan/processor/command/help/filename.rst',
                     'trepan/processor/command/help/location.rst',
                     'trepan/processor/command/help/suffixes.rst',
                     ])],
       description        = short_desc,
       entry_points = {
        'console_scripts': [
            'trepan2  = trepan.cli:main',
            'trepan2c  = trepan.client:main',
        ]},
       install_requires   = install_requires,
       license            = license,
       long_description   = long_description,
       py_modules         = py_modules,
       name               = modname,
       namespace_packages = namespace_packages,
       packages           = packages,
       test_suite         = 'nose.collector',
       url                = web,
       setup_requires     = ['nose>=1.0'],
       version            = version,
       zip_safe           = zip_safe)
