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

import atexit, os
from import_relative import import_relative

# Our local modules
Mdebugger  = import_relative('debugger', '...', 'pydbg')
Mbase_cmd  = import_relative('base_cmd', top_name='pydbg')
Mcomcodes  = import_relative('comcodes', '...interface', 'pydbg')
debugger   = import_relative('debugger', '...')
Mmisc      = import_relative('misc', '...', 'pydbg')

class RestartCommand(Mbase_cmd.DebuggerCommand):
    """restart - Restart debugger and program via an exec
    call. All state is lost, and new copy of the debugger is used."""

    category      = 'support'
    min_args      = 0
    max_args      = 0
    name_aliases  = ('restart', )
    need_stack    = False
    short_help    = '(Hard) restart of program via execv()'

    def run(self, args):
        sys_argv = self.debugger.orig_sys_argv or \
            self.debugger.program_sys_argv
        if sys_argv:
            confirmed = self.confirm('Restart (execv)', False)
            if confirmed: 
                self.msg(Mmisc.wrapped_lines("Re exec'ing:", repr(sys_argv),
                                             self.settings['width']))
                # Run atexit finalize routines. This seems to be Kosher:
                # http://mail.python.org/pipermail/python-dev/2009-February/085791.html
                atexit._run_exitfuncs()
                os.execvp(sys_argv[0], sys_argv)
                pass
            pass
        else:
            self.errmsg("No executable file and command options recorded.")
            pass
        return
    pass

if __name__ == '__main__':
    mock = import_relative('mock')
    d, cp = mock.dbg_setup()
    command = RestartCommand(cp)
    command.run([])
    import sys
    if len(sys.argv) > 1:
        # Strip of arguments so we don't loop in exec.
        d.orig_sys_argv = ['python', sys.argv[0]] 
        command.run([])
        pass
    pass


