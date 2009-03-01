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
import sys

# Our local modules
from import_relative import import_relative

import_relative('lib', '...', 'pydbg')
Mbase_cmd  = import_relative('base_cmd', top_name='pydbg')
Mcmdfns    = import_relative('cmdfns', top_name='pydbg')
Mmisc      = import_relative('misc', '...', 'pydbg')

class PythonCommand(Mbase_cmd.DebuggerCommand):
    """python

Run python as a command subshell.
"""

    category      = 'support'
    min_args      = 0
    max_args      = 0
    name_aliases  = ('python', 'py')
    need_stack    = False
    short_help    = 'Run python as a command subshell'

    def run(self, args):
        # See if python's code module is around
        try:
            from code import interact
        except ImportError:
            self.msg("python code doesn't seem to be importable.")
            return

#         # Python does it's own history thing.
#         # Make sure it doesn't damage ours.
#         if hasattr(self, 'readline') and self.readline:
#             try:
#                 self.debugger.write_history_file()
#             except IOError:
#                 pass

        local = None
        if self.proc.curframe:
            if self.proc.curframe.f_locals:
                local = dict(self.proc.curframe.f_locals)
                local.update(self.proc.curframe.f_globals)
            else:
                local = self.proc.curframe.f_globals
            pass

        if local:
            interact(banner='Pydb python shell (with locals)', local=local)
        else:
            interact(banner='Pydb python shell')
            pass

#         # restore our history if we can do so.
#         if hasattr(self, 'readline') and self.readline and self.histfile is not none:
#             try:
#                 self.readline.read_history_file(self.histfile)
#             except ioerror:
#                 pass
#             return
        return

if __name__ == '__main__':
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    command = PythonCommand(d.core.processor)
    command.proc.frame = sys._getframe()
    command.proc.setup()
    if len(sys.argv) > 1:
        print "Type Python commands and exit to quit"
        print command.run(['python'])
        pass
    pass
