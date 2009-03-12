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
import inspect, os, pyficache, sys, threading

# Our local modules
from import_relative import *

import_relative('lib', '...', 'pydbgr')
Mbase_cmd  = import_relative('base_cmd', top_name='pydbgr')
Mcmdfns    = import_relative('cmdfns', top_name='pydbgr')
Mmisc      = import_relative('misc', '...', 'pydbgr')

try:
    import IPython
    class IPythonCommand(Mbase_cmd.DebuggerCommand):
        """ipython

    Run ipython as a command subshell. You need to have ipython installed
    for this command to work. If no ipython options are
    given the following options are passed: 
      -noconfirm_exit -prompt_in1 'Pydbgr In [\#]: '
    """

        category      = 'support'
        min_args      = 0
        max_args      = 0
        name_aliases  = ('ipython', 'ipy')
        need_stack    = False
        short_help    = 'Run ipython as a command subshell'

        def run(self, args):

            if len(args) > 1:
                argv = args[1:]
            else:
                argv = ['-noconfirm_exit','-prompt_in1', 'Pydbgr In [\\#]: ']
                pass

            if self.proc.curframe and self.proc.curframe.f_locals:
                user_ns = self.proc.curframe.f_locals
            else:
                user_ns = {}
                pass

            # Give ipython and the user a way to get access to the debugger
            # setattr(ipshell, 'debugger', self.debugger)
            user_ns['debugger'] = self.debugger

            # IPython does it's own history thing.
            # Make sure it doesn't damage ours.
            have_line_edit = self.debugger.intf[-1].input.line_edit
            if have_line_edit:
                try:
                    self.proc.write_history_file()
                except IOError:
                    pass
                pass

            if user_ns:
                ipshell = IPython.Shell.IPShellEmbed(argv=argv, user_ns=user_ns)
            else:
                ipshell = IPython.Shell.IPShellEmbed(argv=argv)
                pass


            if hasattr(ipshell.IP, "magic_pydbgr"):
                # We get an infinite loop when doing recursive edits
                self.msg("Removing magic %pydbgr")
                delattr(ipshell.IP, "magic_pydbgr")
            ipshell()
#             # Restore our history if we can do so.
#             if self.readline and self.histfile is not None:
#                 try:
#                     self.readline.read_history_file(self.histfile)
#                 except IOError:
#                     pass
#                 return False
            return False
        pass
    pass
except ImportError:
    pass

if __name__ == '__main__':
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    command = IPythonCommand(d.core.processor)
    command.proc.frame = sys._getframe()
    command.proc.setup()
    if len(sys.argv) > 1:
        print "Type IPython commands and exit to quit"
        print command.run(['ipython'])
        pass
    pass
