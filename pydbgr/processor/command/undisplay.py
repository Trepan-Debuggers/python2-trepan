# -*- coding: utf-8 -*-
#   Copyright (C) 2009, 2010 Rocky Bernstein
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

Mbase_cmd  = import_relative('base_cmd', top_name='pydbgr')

class UndisplayCommand(Mbase_cmd.DebuggerCommand):
    """undisplay display-number..."""
    
    aliases       = ('und',)
    category      = 'data'
    min_args      = 1
    max_args      = None
    name          = os.path.basename(__file__).split('.')[0]
    need_stack    = False
    short_help    = 'Cancel some expressions to be displayed when program stops'

    def run(self, args):
        """Cancel some expressions to be displayed when program stops.
Arguments are the code numbers of the expressions to stop displaying.
No argument means cancel all automatic-display expressions.
"delete display" has the same effect as this command.
Do "info display" to see current list of code numbers.
"""

        if len(args) == 1:
            self.proc.display_mgr.clear()
            return
        for i in args[1:]:
            i = self.proc.get_an_int(i, '%r must be a display number' % i)
            if i is not None:
                if not self.proc.display_mgr.delete_index(i):
                    self.errmsg("No display number %d." % i)
                    return
                pass
            pass
        return False
    pass

if __name__ == '__main__':
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    import inspect
    Mcmdproc     = import_relative('cmdproc', '..')
    Mdebugger    = import_relative('debugger', '...')
    d            = Mdebugger.Debugger()
    cp           = d.core.processor
    command = UndisplayCommand(d.core.processor)
    cp.curframe = inspect.currentframe()
    cp.stack, cp.curindex = Mcmdproc.get_stack(cp.curframe, None, None,
                                               cp)
    command.run(['undisplay', 'z'])
    command.run(['undisplay', '1', '10'])
    pass
