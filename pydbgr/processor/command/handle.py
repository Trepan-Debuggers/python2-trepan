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
Msig       = import_relative('sighandler', '...lib', 'pydbgr')

class HandleCommand(Mbase_cmd.DebuggerCommand):
    """Specify how to handle a signal.
    
Args are signals and actions to apply to those signals.
recognized actions include "stop", "nostop", "print", "noprint",
"pass", "nopass", "ignore", or "noignore".

- Stop means reenter debugger if this signal happens (implies print and
  nopass).
- Print means print a message if this signal happens.
- Pass means let program see this signal; otherwise program doesn't know.
- Ignore is a synonym for nopass and noignore is a synonym for pass.
- Pass and Stop may not be combined. (This is different from gdb)
"""

    category     = 'running'
    min_args      = 1
    max_args      = None
    name_aliases = ('handle',)
    need_stack    = False
    short_help    = "Specify how to handle a signal"
    
    def run(self, args):
        self.debugger.sigmgr.action(' '.join(args[1:]))
        return 
    pass

if __name__ == '__main__':
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    command = HandleCommand(d.core.processor)
    command.run(['handle', 'term', 'stop'])
    pass


