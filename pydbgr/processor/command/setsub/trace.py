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

import tracer
from import_relative import *
base_subcmd  = import_relative('base_subcmd', '..')
cmdfns       = import_relative('cmdfns', '..')
short_help   = "Set execution tracing, delay and event set."


class SetTrace(base_subcmd.DebuggerSubcommand):

    """Set trace [on|off] [EVENT...]

Turns line tracing on or off and/or the event mask to filter shown
events. "all" can be used as an abbreviation for listing all event
names. See the "step" command for a list of event names.

Changing trace event filters works independently of turning on or off
tracing-event printing.

Examples: 
  set trace on     # Turn on event tracing. Trace filters are unchanged.
  set trace        # Same as above.
  set trace off    # Turn off event tracing. Trace filters are unchanged.
  set trace line   # Set trace filter for line events only. On/off status 
                   # doesn't change.
  set trace call return on # Trace calls and returns only; turn on tracing.
  set trace all    # Set trace filter to all events. On/off status unchanged.
  set trace all on # Set trace filter to all events; turn on tracing.

See also "show trace".
"""

    in_list    = True
    min_abbrev = 2  # Must use at least "set tr"
    short_help = "Set execution tracing and trace filter"

    def run(self, args):
        if 0 == len(args): args = ['on']
        valid_args = tracer.ALL_EVENT_NAMES + ('on', 'off', 'all')
        on_off = None
        eventset = []
        for arg in args:
            if arg not in valid_args:
                self.errmsg('set trace: Invalid argument %s ignored.' % arg)
                continue
            if arg in tracer.ALL_EVENTS:
                eventset += [arg]
            elif 'all' == arg:
                eventset += tracer.ALL_EVENTS
            elif on_off is not None:
                self.errmsg('set trace: Duplicate on/off value %s ignored.' 
                            % arg)
            else:
                on_off = arg
                pass
            pass
        if [] != eventset:
            self.debugger.settings['printset'] = frozenset(eventset)
            pass
        if on_off is not None:
            cmdfns.run_set_bool(self, [on_off])
            pass
        return

    pass

if __name__ == '__main__':
    mock = import_relative('mock', '..')
    Mset = import_relative('set', '..')
    d, cp = mock.dbg_setup()
    s = Mset.SetCommand(cp)
    sub = SetTrace(s)
    sub.name = 'trace'
    for args in (['on'], ['off'], ['line'], ['bogus'],
                ['on', 'call', 'return']):
        sub.run(args)
        print d.settings['printset']
        print d.settings['trace']
        pass
    pass
