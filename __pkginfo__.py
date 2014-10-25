# Copyright (C) 2008-2010, 2013-2014 Rocky Bernstein <rocky@gnu.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Debugger packaging information"""

# To the extent possible we make this file look more like a
# configuration file rather than code like setup.py. I find putting
# configuration stuff in the middle of a function call in setup.py,
# which for example requires commas in between parameters, is a little
# less elegant than having it here with reduced code, albeit there
# still is some room for improvement.

# Things that change more often go here.
copyright   = """
Copyright (C) 2008-2010, 2013-2014 Rocky Bernstein <rocky@gnu.org>.
"""

classifiers =  ['Development Status :: 4 - Beta',
                'Environment :: Console',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: GNU General Public License (GPL)',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Topic :: Software Development :: Debuggers',
                'Topic :: Software Development :: Libraries :: Python Modules',
                ]

# The rest in alphabetic order
author             = "Rocky Bernstein"
author_email       = "rocky@gnu.org"
ftp_url            = None
install_requires   = ['columnize >= 0.3.4',
                      'import_relative >= 0.2.3',
                      'pyficache >= 0.2.3',
                      'pygments',
                      'tracer >= 0.3.2']
license            = 'GPL'
mailing_list       = 'python-debugger@googlegroups.com'
modname            = 'trepan'
namespace_packages = [
    'trepan',
]
packages           = namespace_packages
py_modules         = None
short_desc         = 'Modular Python Debugger'

import os
import os.path, sys


def get_srcdir():
    """Get directory of caller as an absolute file name. *level* is
    the number of frames to look back.  So for import file which is
    really doing work on behalf of *its* caller, we go back 2.

    NB: f_code.co_filenames and thus this code kind of broken for
    zip'ed eggs circa Jan 2009
    """

    caller = sys._getframe(1)
    filename = caller.f_code.co_filename
    filename = os.path.normcase(os.path.dirname(os.path.abspath(filename)))
    return os.path.realpath(filename)

# VERSION.py sets variable VERSION.
execfile(os.path.join(get_srcdir(), 'trepan', 'VERSION.py'))
version            = VERSION  # NOQA
web                = 'http://github.com/rocky/python-trepan2/'

# tracebacks in zip files are funky and not debuggable
zip_safe = False


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()
long_description   = ( read("README.md") + '\n\n' +  read("NEWS") )
