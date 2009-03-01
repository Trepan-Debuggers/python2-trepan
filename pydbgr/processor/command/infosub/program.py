# -*- coding: utf-8 -*-
#   Copyright (C) 2008, 2009 Rocky Bernstein <rocky@gnu.org>
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

from import_relative import *
# Our local modules
# FIXME: Until import_relative is fixed up...
import_relative('processor', '....', 'pydbg')
Mbase_subcmd  = import_relative('base_subcmd', '..', 'pydbg')
Mmisc         = import_relative('misc', '....', 'pydbg')

class InfoProgram(Mbase_subcmd.DebuggerSubcommand):
    'Execution status of the program.'

    min_abbrev = 1 # Need at least info p
    need_stack = True
    short_help = 'Execution status of the program'

    def run(self, args):
        """Execution status of the program."""
        mainfile = self.core.filename(None)
        if self.core.is_running():
            if mainfile:
                part1 = "Python program '%s' is stopped" % mainfile 
            else:
                part1 = 'Program is stopped'
                pass
            if self.proc.event:
                msg = 'via event: "%s".' % self.proc.event
            else:
                msg = '.'
            self.msg(Mmisc.wrapped_lines(part1, msg,
                                         self.settings['width']))
            if self.proc.event == 'return': 
                val = self.proc.event_arg
                part1 = 'Return value is'
                self.msg(Mmisc.wrapped_lines(part1, self.proc._saferepr(val),
                                             self.settings['width']))
                pass
            self.msg('It stopped %s.' % self.core.stop_reason)
        else:
            if mainfile:
                part1 = "Python program '%s'" % mainfile
                msg   = "is not currently running. " 
                self.msg(Mmisc.wrapped_lines(part1, msg,
                                             self.settings['width']))
            else:
                msg = 'No Python program is currently running. '
                pass
            msg += self.core.execution_status
            self.msg(msg)
            pass
        return False
    pass

if __name__ == '__main__':
    mock = import_relative('mock', '..')
    Minfo = import_relative('info', '..')
    Mdebugger = import_relative('debugger', '....')
    d = Mdebugger.Debugger()
    d, cp = mock.dbg_setup(d)
    i = Minfo.InfoCommand(cp)
    sub = InfoProgram(i)
    sub.run([])
