# -*- coding: utf-8 -*-
#   Copyright (C) 2012 Rocky Bernstein
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
from pyficache import clear_file_format_cache

# Our local modules
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')

class SetHighlight(Mbase_subcmd.DebuggerSetBoolSubcommand):
    """Set whether we use terminal highlighting"""

    in_list    = True
    min_abbrev = len('hi')

    def run(self, args):
        if len(args) == 1 and 'reset' == args[0]:
            clear_file_format_cache
            self.settings['highlight'] = 'terminal'
        else:
            # I haven't been able to figure out how to use super() to
            # shorten this:
            Mbase_subcmd.DebuggerSetBoolSubcommand.run(self, args)

            # The above makes settings['highlight'] be a boolean, but
            # we want it to be either 'terminal' or 'plain'
            if self.settings['highlight']:
                self.settings['highlight'] = 'terminal'
            else:
                self.settings['highlight'] = 'plain'
            pass
        return
    pass



