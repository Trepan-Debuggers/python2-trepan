# -*- coding: utf-8 -*-
#  Copyright (C) 2015 Rocky Bernstein
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os, sys
from sys import version_info

# Our local modules
from trepan.processor.command import base_cmd as Mbase_cmd

class PythonCommand(Mbase_cmd.DebuggerCommand):
    """**deparse** [offset]

deparse around where the program is currently stopped. If no offset is given
we use the current frame offset.
"""

    category      = 'data'
    min_args      = 0
    max_args      = 1
    name          = os.path.basename(__file__).split('.')[0]
    need_stack    = True
    short_help    = 'Deparse source via uncompyle'

    def run(self, args):
        # Can't do anything if we don't have python deparse
        try:
            from trepan_deparse import deparser
        except ImportError:
            self.errmsg("deparse needs to be installed to run this command")
            return

        co = self.proc.curframe.f_code

        if len(args) == 2:
            last_i = self.proc.get_an_int(args[1],
                                          ("The 'deparse' command when given an argument requires an"
                                           " instruction offset. Got: %s") %
                                          args[1])
        else:
            last_i = self.proc.curframe.f_lasti

        if last_i == -1:
            if co.co_name:
                self.msg("At beginning of %s " % co.co_name)
                return
            elif self.core.filename(None):
                self.msg("At beginning of program %s" % self.core.filename(None))
                return
            else:
                self.msg("At beginning")
                return

        sys_version = version_info.major + (version_info.minor / 10.0)
        try:
            walk = deparser.deparse(sys_version, co)
        except:
            self.errmsg("error in deparsing code at %d" % last_i)
            return
        if last_i in sorted(walk.offsets.keys()):
            extractInfo = walk.extract_line_info(last_i)
            print extractInfo
            self.msg(extractInfo.selectedLine)
            self.msg(extractInfo.markerLine)
        else:
            self.errmsg("cant find %d" % last_i)
            print sorted(walk.offsets.keys())
        return
    pass

# if __name__ == '__main__':
#     from trepan import debugger as Mdebugger
#     d = Mdebugger.Debugger()
#     command = PythonCommand(d.core.processor)
#     command.proc.frame = sys._getframe()
#     command.proc.setup()
#     if len(sys.argv) > 1:
#         print("Type Python commands and exit to quit.")
#         print(sys.argv[1])
#         if sys.argv[1] == '-d':
#             print(command.run(['bpy', '-d']))
#         else:
#             print(command.run(['bpy']))
#             pass
#         pass
#     pass
