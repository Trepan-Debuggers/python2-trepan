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
Mbase_cmd  = import_relative('base_cmd')
Mprint     = import_relative('lib.print', '...')

class ExamineCommand(Mbase_cmd.DebuggerCommand):

    category     = 'data'
    min_args      = 1
    max_args      = None
    name_aliases = ('examine','x')
    need_stack    = True
    short_help    = "Examine value, type and object attributes of an expression"

    def run(self, args):
        """examine expr1 [expr2 ...]

        Examine value, type and object attributes of an expression."""
        
        for arg in args[1:]:
            s = Mprint.print_obj(arg, self.proc.curframe)
            self.msg(s)
            pass
        return 

    pass

if __name__ == '__main__':
    mock = import_relative('mock')
    d, cp = mock.dbg_setup()
    command = ExamineCommand(cp)
    pass


