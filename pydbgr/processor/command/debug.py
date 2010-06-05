# -*- coding: utf-8 -*-
#  Copyright (C) 2010 Rocky Bernstein
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

import os, sys, threading
from import_relative import import_relative
Mbase_cmd  = import_relative('base_cmd', top_name='pydbgr')
Mdebugger  = import_relative('debugger', '...', top_name='pydbgr')

class DebugCommand(Mbase_cmd.DebuggerCommand):
    """debug PYTHON-EXPR
    
Enter a nested debugger that steps through the PYTHON-CODE argument
which is an arbitrary expression to be executed the current
environment."""

    category     = 'support'
    min_args      = 1
    max_args      = None
    name          = os.path.basename(__file__).split('.')[0]
    need_stack    = True
    short_help    = 'Debug PYTHON-EXPR'

    def run(self, args):
        arg = ' '.join(args[1:])
        curframe = self.proc.curframe
        if not curframe:
            self.msg("No frame selected.")
            return
        old_prompt_str            = self.proc.prompt_str
        old_lock                  = self.core.debugger_lock
        old_stop_level            = self.core.stop_level
        old_different_line        = self.core.stop_level
        self.proc.prompt_str      = "(%s) " % old_prompt_str.strip()
        self.core.debugger_lock   = threading.Lock()
        self.core.stop_level      = None
        self.core.different_line  = None
        global_vars               = curframe.f_globals
        local_vars                = curframe.f_locals

        print "stop_level: %s, different_line: %s " % (self.core.stop_level,
                                                       self.core.different_line)
        self.msg("ENTERING NESTED DEBUGGER")

        sys.call_tracing(eval, (arg, global_vars, local_vars))
        self.msg("LEAVING NESTED DEBUGGER")

        self.proc.prompt_str      = old_prompt_str
        self.core.debugger_lock   = old_lock
        self.core.stop_level      = old_stop_level
        self.core.different_line  = old_different_line
        self.proc.print_location()
        return False
    pass

if __name__ == '__main__':
    import inspect
    Mcmdproc    = import_relative('cmdproc', '..', 'pydbgr')
    debugger    = import_relative('debugger', '...')
    d           = debugger.Debugger()
    cp          = d.core.processor
    cp.curframe = inspect.currentframe()
    cp.stack, cp.curindex = Mcmdproc.get_stack(cp.curframe, None, None,
                                               cp)
    command = DebugCommand(cp)
    def test_fn():
        return 5
    command.run(['debug', 'test_fn()'])
    pass
