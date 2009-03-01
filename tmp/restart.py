# -*- coding: utf-8 -*-
#   Copyright (C) 2009 Rocky Bernstein
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
#    02110-1301 USA.
import inspect, os, sys, threading
from import_relative import *

# Our local modules
base_cmd  = import_relative('base_cmd')
topsrcdir = os.path.join(os.path.pardir, os.path.pardir)
debugger  = import_relative('debugger', topsrcdir)
from debugger import DebuggerQuit
from cmdfns import *

class RestartCommand(base_cmd.DebuggerCommand):
    """restart - Restart debugger and program via an exec
call. All state is lost, and new copy of the debugger is used."""

    category      = 'support'
    min_args      = 0
    max_args      = 0
    name_aliases  = ('restart', 'R',)
    need_stack    = False

    def run(self, args):
        if hasattr(self.debugger, '_program_sys_argv'):
            confirmed = self.confirm('Hard restart')
            if confirmed: 
                sys_argv = self.debugger._program_sys_argv
                if sys_argv[0]:
                    self.msg("Re exec'ing:\n\t%s" % sys_argv)
                    os.execvp(sys_argv[0], sys_argv)
                else:
                    self.errmsg("No exectuable file specified.")
                    pass
                pass
            pass
        else:
            self.errmsg("Command arguments not found.")
        return False
    pass

if __name__ == '__main__':
    mock = import_relative('mock')
    d, cp = mock.dbg_setup()
    command = RestartCommand(cp)
    pass


