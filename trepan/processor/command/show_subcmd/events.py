# -*- coding: utf-8 -*-
#   Copyright (C) 2009, 2015 Rocky Bernstein
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

import columnize

# Our local modules
from trepan.processor.command import base_subcmd as Mbase_subcmd


class ShowEvents(Mbase_subcmd.DebuggerSubcommand):
    """**show events**

Show the kinds of events the debugger will stop on.

See also:
---------

`set events`. `help step` lists of event names.
"""
    min_abbrev = 2
    short_help = 'Show the kinds of events the debugger will stop on'

    def run(self, args):
        events = list(self.debugger.settings['printset'])
        if events != []:
            events.sort()
            self.section('Trace events we may stop on:')
            self.msg(columnize.columnize(events, lineprefix='    '))
        else:
            self.msg('No events trapped.')
            return
        return
    pass

if __name__ == '__main__':
    from trepan.processor.command import mock, show as Mshow
    from trepan import debugger as Mdebugger
    d = Mdebugger.Debugger()
    d, cp = mock.dbg_setup(d)
    i = Mshow.ShowCommand(cp)
    sub = ShowEvents(i)
    sub.run([])
    pass
