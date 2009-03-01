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

# Our local modules
from import_relative import import_relative

import_relative('lib', '...', 'pydbg')
Mbase_cmd  = import_relative('base_cmd', top_name='pydbg')
Mcmdfns    = import_relative('cmdfns', top_name='pydbg')
Mfile      = import_relative('lib.file', '...', 'pydbg')
Mmisc      = import_relative('misc', '...', 'pydbg')
Mbreak     = import_relative('break', '.', 'pydbg')

class DeleteCommand(Mbase_cmd.DebuggerCommand):
    """delete [bpnumber [bpnumber...]]  - Delete some breakpoints.

Arguments are breakpoint numbers with spaces in between.  To delete
all breakpoints, give no argument.  those breakpoints.  Without
argument, clear all breaks (but first ask confirmation).
    
See also the 'clear' command which clears breakpoints by line/file
number.."""

    category      = 'breakpoints'
    min_args      = 0
    max_args      = None
    name_aliases  = ('delete',)
    need_stack    = False
    short_help    = 'Delete some breakpoints or auto-display expressions'

    def run(self, args):
        if len(args) <= 1:
            if self.confirm('Delete all breakpoints', False):
                self.core.bpmgr.delete_all_breakpoints()
            return

        for arg in args[1:]:
            try:
                i = self.get_pos_int(self.errmsg, arg, min_value=1, 
                                     default=None,
                                     cmdname='delete')
            except ValueError:
                continue

            success, msg = self.core.bpmgr.delete_breakpoint_by_number(i)
            if not success:
                self.errmsg(msg)
            else:
                self.msg('Deleted breakpoint %d' % i)
                pass
            pass
        return
        

if __name__ == '__main__':
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    command = DeleteCommand(d.core.processor)
    pass
