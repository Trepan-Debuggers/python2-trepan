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
from import_relative import import_relative

# Our local modules
Mbase_cmd  = import_relative('base_cmd', top_name='pydbg')
Mcmdfns   = import_relative('cmdfns', top_name='pydbg')

class ExitCommand(Mbase_cmd.DebuggerCommand):

    category      = 'support'
    min_args      = 0
    max_args      = 1
    name_aliases  = ('exit',)
    need_stack    = True
    short_help    = 'Exit program via sys.exit()'

    def run(self, args):
        """exit [exitcode] - hard exit of the debugged program.  

The program being debugged is exited via sys.exit(). If a return code
is given that is the return code passed to sys.exit() - presumably the
return code that will be passed back to the OS."""

        self.core.stop()
        self.core.execution_status = 'Exit command'
        if len(args) <= 1:
            exitcode = 0
        else:
            try:
                exitcode = Mcmdfns.get_pos_int(self.errmsg, args[1], default=0,
                                               cmdname='exit')
            except ValueError:
                return False
            pass
        # FIXME: allow setting a return code.
        import sys
        sys.exit(exitcode)
        # Not reached
        return True

# Demo it
if __name__ == '__main__':
    mock = import_relative('mock')
    d, cp = mock.dbg_setup()
    command = ExitCommand(cp)
    command.run(['exit', 'wrong', 'number', 'of', 'args'])
    command.run(['exit', 'foo'])
    command.run(['exit', '10'])
