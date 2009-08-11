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
import inspect, os
from import_relative import import_relative

# Our local modules
Mbase_cmd  = import_relative('base_cmd', top_name='pydbgr')
Mcmdproc   = import_relative('cmdproc', '..', 'pydbgr')
Mcmdfns    = import_relative('cmdfns', top_name='pydbgr')

class JumpCommand(Mbase_cmd.DebuggerCommand):

    aliases       = ('j',)
    category      = 'running'
    execution_set = ['Running']
    min_args      = 1
    max_args      = 1
    name          = os.path.basename(__file__).split('.')[0]
    need_stack    = False
    short_help    = 'Set the next line to be executed'

    def run(self, args):
        """jump lineno

        Set the next line that will be executed. The line must be within
        the stopped or bottom-most execution frame frame."""

        if not self.core.is_running(): return False

        if self.proc.curindex + 1 != len(self.proc.stack):
            self.errmsg("You can only jump within the bottom frame")
            return False

        if self.proc.curframe.f_trace is None:
            self.errmsg("Sigh - operation can't be done here.")
            return False

        lineno = self.proc.get_an_int(args[1],
                                      ("jump: a line number is required, " +
                                       "got %s.") % args[1])
        if lineno is None: return False
        try:
            # Set to change position, update our copy of the stack,
            # and display the new position
            print self.proc.curframe.f_trace
            self.proc.curframe.f_lineno = lineno
            self.proc.stack[self.proc.curindex] = \
                self.proc.stack[self.proc.curindex][0], lineno
            Mcmdproc.print_location(self.proc)
        except ValueError, e:
            self.errmsg('jump failed: %s' % e)
        return False
    pass

if __name__ == '__main__':
    mock = import_relative('mock')
    d, cp = mock.dbg_setup()
    command = JumpCommand(cp)
    print 'jump when not running: ', command.run(['jump', '1'])
    command.core.execution_status = 'Running'
    cp.curframe = inspect.currentframe()
    cp.curindex = 0
    cp.stack = Mcmdproc.get_stack(cp.curframe, None, None)
    command.run(['jump', '1'])
    cp.curindex = len(cp.stack)-1
    command.run(['jump', '1'])
    pass


