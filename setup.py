#!/usr/bin/env python

"""
distutils setup (setup.py).

This is just boilerplate code, since we do like to try to keep data separate
from code as much as possible. The customizable information really comes
from file __pkginfo__.py.
"""

import os, sys

if not ((2, 4) <= sys.version_info[0:2] < (3, 0)):
    mess = "Only Python Versions 2.4 to 2.7 are supported in this package."
    if (3, 2) <= sys.version_info[0:2] < (3, 7):
        mess += "\nFor your Python, version %s, see trepan3k" % sys.version[0:3]
    elif sys.version_info[0:2] < (2, 6):
        mess += "\nFor your Python, version %s, see pydbgr" % sys.version[0:3]
    raise Exception(mess)
elif ((2, 4) <= sys.version_info[0:2] < (2, 6)) and not os.path.exists(
    "gitbranch-master"
):
    raise Exception("You have the wrong code or git branch for Python 2.4, 2.5")


# Get the package information used in setup().
from __pkginfo__ import (
    author,
    author_email,
    classifiers,
    install_requires,
    license,
    long_description,
    modname,
    packages,
    py_modules,
    short_desc,
    version,
    web,
    zip_safe,
)

__import__("pkg_resources")
from setuptools import setup

setup(
    author=author,
    author_email=author_email,
    classifiers=classifiers,
    data_files=[
        (
            "trepan/processor/command/help",
            [
                "trepan/processor/command/help/arange.rst",
                "trepan/processor/command/help/command.rst",
                "trepan/processor/command/help/examples.rst",
                "trepan/processor/command/help/filename.rst",
                "trepan/processor/command/help/location.rst",
                "trepan/processor/command/help/range.rst",
                "trepan/processor/command/help/suffixes.rst",
            ],
        )
    ],
    description=short_desc,
    entry_points={
        "console_scripts": [
            "trepan2  = trepan.cli:main",
            "trepan2c  = trepan.client:main",
        ]
    },
    install_requires=install_requires,
    license=license,
    long_description=long_description,
    py_modules=py_modules,
    name=modname,
    packages=packages,
    test_suite="nose.collector",
    url=web,
    version=version,
    zip_safe=zip_safe,
)
