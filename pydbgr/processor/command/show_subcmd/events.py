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

from import_relative import *
# Our local modules
base_subcmd  = import_relative('base_subcmd', os.path.pardir)
cmdfns       = import_relative('cmdfns', os.path.pardir)
class ShowEvents(base_subcmd.DebuggerSubcommand):
    '''Show trace events we may stop on.'''
    min_abbrev = 2
    run_cmd    = False

    run = cmdfns.run_show_val
    pass

if __name__ == '__main__':
    mock = import_relative('mock', '..')
    Mshow = import_relative('show', '..')
    Mdebugger = import_relative('debugger', '....')
    d = Mdebugger.Debugger()
    d, cp = mock.dbg_setup(d)
    i = Mshow.ShowCommand(cp)
    sub = ShowEvents(i)
    sub.run([])
    pass
