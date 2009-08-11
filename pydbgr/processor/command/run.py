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
import os
from import_relative import import_relative

# Our local modules
Mbase_cmd  = import_relative('base_cmd', top_name='pydbgr')
Mexcept    = import_relative('exception', '...', 'pydbgr')

class RunCommand(Mbase_cmd.DebuggerCommand):
    """restart - Restart debugger and program via an exec
call. All state is lost, and new copy of the debugger is used."""

    aliases       = ('R',)
    category      = 'support'
    min_args      = 0
    max_args      = 0
    name          = os.path.basename(__file__).split('.')[0]
    need_stack    = False
    short_help    = '(Soft) restart program via a DebuggerRestart exception'

    def run(self, args):
        confirmed = self.confirm('Restart', False)
        if confirmed: 
            self.core.step_ignore = 0
            self.core.step_events = None
            raise Mexcept.DebuggerRestart(self.core.debugger.restart_argv())
        pass
    pass

if __name__ == '__main__':
    mock = import_relative('mock')
    d, cp = mock.dbg_setup()
    command = RunCommand(cp)
    try:
        command.run([])
    except Mexcept.DebuggerRestart:
        import sys
        print 'Got restart exception: parms ', sys.exc_value.sys_argv
        pass
    pass


