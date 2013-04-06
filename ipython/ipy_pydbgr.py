# -*- coding: utf-8 -*-
#   Copyright (C) 2008, 2009 Rocky Bernstein <rocky@gnu.org>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Imported this when running IPython to cut over debugging stuff to use
# trepan. There is much, much, much room for improvement.
try:
    import trepan.post_mortem, trepan.cli
except ImportError:
    raise ImportError("Sorry - trepan doesn't seem to be installed.")

try:
    import IPython.ipapi
except ImportError:
    raise ImportError("IPython doesn't seem to be installed.")

from IPython.genutils import arg_split
from trepan.debugger import Debugger

ip = IPython.ipapi.get()

if not ip:
    raise ImportError("IPython isn't running")

def ipy_trepan_post_mortem(force=False):
    '''A trepan replacement for IPython's iplib.debugger.
    The routine is called when IPython hits an exception and
    the user has indicated they want to go into post-mortem
    debugging for this.
    '''
    if not (force or __IPYTHON__.call_pdb): return
    __IPYTHON__.history_saving_wrapper(trepan.post_mortem.pm)()
    return

__IPYTHON__.debugger = ipy_trepan_post_mortem
__IPYTHON__.InteractiveTB.debugger = ipy_trepan_post_mortem

def ipy_trepan(self, args):
    '''Call the trepan debugger.'''
    sys_argv = ['cli.py'] + arg_split(args)
    dbg = Debugger()

    # This is broken. For now I'd rather switch than fight it.
    # __IPYTHON__.history_saving_wrapper(trepan.cli.main(sys_argv=argv))()
    trepan.cli.main(dbg, sys_argv)
    return

ip.expose_magic('trepan', ipy_trepan)
