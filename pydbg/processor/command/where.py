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
Mbase_cmd = import_relative('base_cmd', top_name='pydbg')
Mstack    = import_relative('stack', '...lib', 'pydbg')
Mcmdfns   = import_relative('cmdfns', top_name='pydbg')

class WhereCommand(Mbase_cmd.DebuggerCommand):

    category      = 'stack'
    min_args      = 0
    max_args      = 1
    name_aliases  = ('where', 'bt', 'backtrace')
    need_stack    = True
    short_help   = 'Print backtrace of stack frames'

    def run(self, args):
        """where [count]

Print a stack trace, with the most recent frame at the top.  With a
positive number, print at most many entries.  An arrow indicates the
'current frame'. The current frame determines the context used for 
many debugger commands such as expression evaluation or source-line listing.
"""

        if len(args) > 1:
            try:
                count = Mcmdfns.get_pos_int(self.errmsg, args[1], default=None, 
                                            cmdname="where")
            except ValueError:
                return False
            pass
        else:
            count = None
            pass

        if not self.proc.curframe:
            self.errmsg("No stack.")
            return False
        Mstack.print_stack_trace(self.proc, count)
        return False

    pass

if __name__ == '__main__':
    cmdproc      = import_relative('cmdproc', '..')
    debugger     = import_relative('debugger', '...')
    d            = debugger.Debugger()
    cp           = d.core.processor
    command      = WhereCommand(cp)
    command.run(['where', 'wrong', 'number', 'of', 'args'])

    def nest_me(cp, command, i):
        import inspect
        if i > 1:
            cp.curframe = inspect.currentframe()
            cp.stack, cp.curindex = cmdproc.get_stack(cp.curframe, None, None,
                                                      cp)
            print '-' * 10
            command.run(['where'])
            print '-' * 10
            command.run(['where', '1'])
        else:
            nest_me(cp, command, i+1)
        return
    def ignore_me(cp, command, i):
        print '=' * 10
        nest_me(cp, command, 1)
        print '=' * 10
        cp.core.add_ignore(ignore_me)
        nest_me(cp, command, 1)
        return
    cp.forget()
    command.run(['where'])
    ignore_me(cp, command, 1)
    pass

