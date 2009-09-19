# -*- coding: utf-8 -*-
#   Copyright (C) 2009 Rocky Bernstein
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from import_relative import import_relative
# Our local modules
import_relative('processor', '....', 'pydbgr')
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')
Mcmdfns      = import_relative('cmdfns', '..', 'pydbgr')
Mcmdproc     = import_relative('cmdproc', '...', 'pydbgr')

class SetAutoPython(Mbase_subcmd.DebuggerSetBoolSubcommand):
    """Go into Python on debugger entry."""
    
    in_list    = True
    min_abbrev = len('autopy') # Need at least "set autopy"

    python_cmd = None
    
    def run(self, args):
        Mcmdfns.run_set_bool(self, args)
        if self.settings['autopython']:
            if self.python_cmd == None:
                self.python_cmd = self.proc.name2cmd['python'].run
                pass
            self.proc.add_preloop_hook(self.run_python, -1)
        else:
            self.proc.remove_preloop_hook(self.run_python)
            pass
        return

    def run_python(self, args):
        leave_loop = self.python_cmd(['python'])
        if not leave_loop: Mcmdproc.print_location(self.proc)
        return leave_loop

    pass
