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

try:
    import IPython

    from import_relative import import_relative
    # Our local modules
    import_relative('processor', '....', 'pydbgr')
    Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')
    Mcmdfns      = import_relative('cmdfns', '..', 'pydbgr')
    Mcmdproc     = import_relative('cmdproc', '...', 'pydbgr')
    
    class SetAutoIPython(Mbase_subcmd.DebuggerSetBoolSubcommand):
        """Go into IPython on debugger entry."""

        in_list    = True
        min_abbrev = len('autoipy') # Need at least "set autoipy"

        ipython_cmd = None
    
        def run(self, args):
            Mcmdfns.run_set_bool(self, args)
            if self.settings['autoipython']:
                if self.ipython_cmd == None:
                    self.ipython_cmd = self.proc.name2cmd['ipython'].run
                    pass
                self.proc.add_preloop_hook(self.run_ipython, -1)
            else:
                self.proc.remove_preloop_hook(self.run_ipython)
                pass
            return

        def run_ipython(self, args):
            leave_loop = self.ipython_cmd(['ipython'])
            if not leave_loop: Mcmdproc.print_location(self.proc)
            return leave_loop

        pass
except ImportError:
    pass


