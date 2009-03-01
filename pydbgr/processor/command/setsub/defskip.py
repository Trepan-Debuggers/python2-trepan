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
import_relative('processor', '....', 'pydbg')
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbg')

class SetDefSkip(Mbase_subcmd.DebuggerSetBoolSubcommand):
    """Set stopping before 'def' (method creation) statements.

Classes may have many methods and stand-alone programs may have many
functions. Generally there isn't much value to stopping before adding
a method or function to Python's symbol table. (More to the point, it
can be an annoyance.) However if you do want this, e.g. you want to
debug methods is over-writing one another, then set this 'off'."""
    in_list    = True
    min_abbrev = 4    # Min 'set defs'
    short_help="Set stopping before 'def' (method creation) statements"

    pass


