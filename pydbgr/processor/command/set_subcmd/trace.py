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
Mbase_subcmd  = import_relative('base_subcmd', '..', 'pydbgr')


class SetTrace(Mbase_subcmd.DebuggerSetBoolSubcommand):

    """Set trace [on|off]

Turns event tracing on or off.

See also "set events","set trace", and "show trace".
"""

    in_list    = True
    min_abbrev = len('trace')  # Must use at least "set trace"
    short_help = "Set execution tracing"
    pass

if __name__ == '__main__':
    mock = import_relative('mock', '..')
    Mset = import_relative('set', '..')
    d, cp = mock.dbg_setup()
    s = Mset.SetCommand(cp)
    sub = SetTrace(s)
    sub.name = 'trace'
    for args in (['on'], ['off']):
        sub.run(args)
        print d.settings['trace']
        pass
    pass
