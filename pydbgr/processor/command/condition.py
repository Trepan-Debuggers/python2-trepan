# -*- coding: utf-8 -*-
#  Copyright (C) 2009, 2010 Rocky Bernstein
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

import os
from import_relative import import_relative

import_relative('lib', '...', 'pydbgr')
Mbase_cmd  = import_relative('base_cmd', top_name='pydbgr')
Mcmdfns    = import_relative('cmdfns', top_name='pydbgr')
Mfile      = import_relative('file', '...lib', 'pydbgr')
Mmisc      = import_relative('misc', '...', 'pydbgr')

class ConditionCommand(Mbase_cmd.DebuggerCommand):
    """condition BP_NUMBER CONDITION

BP_NUMBER is a breakpoint number.  CONDITION is an expression which
must evaluate to True before the breakpoint is honored.  If CONDITION
is absent, any existing condition is removed; i.e., the breakpoint is
made unconditional.

Examples:
   condition 5 x > 10  # Breakpoint 5 now has condition x > 10
   condition 5         # Remove above condition
"""

    aliases       = ('cond',)
    category      = 'breakpoints'
    min_args      = 1
    max_args      = None
    name          = os.path.basename(__file__).split('.')[0]
    need_stack    = False
    short_help    = 'Specify breakpoint number N to break only if COND is True'

    def run(self, args):
        success, msg, bp = self.core.bpmgr.get_breakpoint(args[1])
        if not success: 
            self.errmsg(msg)
            return
        if len(args) > 2:
            condition = ' '.join(args[2:])
        else:
            condition = None
            self.msg('Breakpoint %d is now unconditional.' % bp.number)
            pass
        bp.condition = condition
        return 

if __name__ == '__main__':
    import sys
    Mdebugger = import_relative('debugger', '...')
    Mbreak    = import_relative('break', '.')
    d = Mdebugger.Debugger()
    brkcmd = Mbreak.BreakCommand(d.core.processor)
    command = ConditionCommand(d.core.processor)
    command.proc.frame = sys._getframe()
    command.proc.setup()

    command.run(['condition', '1'])
    brkcmd.run(['break'])
    command.run(['condition', '1'])
    command.run(['condition', '1', 'x', '>', '10'])
    command.run(['condition', '1'])
    pass
