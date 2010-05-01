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

import os, sys
from import_relative import import_relative
Mbase_cmd  = import_relative('base_cmd', top_name='pydbgr')
Mdebugger  = import_relative('debugger', '...', top_name='pydbgr')

class DebugCommand(Mbase_cmd.DebuggerCommand):
    """debug PYTHON-EXPR
    
Enter a nested debugger that steps through the PYTHON-CODE argument
which is an arbitrary expression or statement to be executed
 the current environment."""

    category     = 'support'
    min_args      = 1
    max_args      = None
    name          = os.path.basename(__file__).split('.')[0]
    need_stack    = True
    short_help    = 'Debug PYTHON-EXPR'

    def run(self, args):
        self.errmsg('Not implemented yet')
        return False
        arg = ' '.join(args[1:])
        curframe = self.proc.curframe
        if not curframe:
            self.msg("No frame selected.")
            return
        self.core.stop
        global_vars = curframe.f_globals
        local_vars = curframe.f_locals
        dbgr = Mdebugger.Debugger()
        cmdproc = dbgr.core.processor
        cmdproc.prompt_str  = "(%s) " % self.proc.prompt_str.strip()
        self.msg("ENTERING NESTED DEBUGGER")

        # Inherit some values from current environment
        cmdproc.aliases   = self.aliases
        cmdproc.settings  = self.proc.settings

        dbgr.run_eval(arg, {'force' : True}, global_vars, local_vars)
        self.msg("LEAVING NESTED DEBUGGER")
        self.core.start
        self.proc.last_command = cmdproc.last_command
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
