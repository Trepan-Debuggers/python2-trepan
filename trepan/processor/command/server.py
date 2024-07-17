# -*- coding: utf-8 -*-
#   Copyright (C) 2016 Rocky Bernstein
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
import os, sys

# Our local modules
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import complete as Mcomplete, file as Mfile
from trepan.interfaces import server as Mserver
from trepan import debugger as Mdebugger


class ServerCommand(Mbase_cmd.DebuggerCommand):
    """**server** [**-v**][**-Y**|**-N**][**-c**] *file*

Read debugger commands from a file named *file*.  Optional *-v* switch
(before the filename) causes each command in *file* to be echoed as it
is executed.  Option *-Y* sets the default value in any confirmation
command to be "yes" and *-N* sets the default value to "no".

Note that the command startup file `.trepanc` is read automatically
via a *source* command the debugger is started.

An error in any command terminates execution of the command file
unless option `-c` is given."""

    category      = 'support'
    min_args      = 1
    max_args      = None
    name          = os.path.basename(__file__).split('.')[0]
    need_stack    = False
    short_help    = "Read and run debugger commands from a file"

    def run(self, args):
        # Push a new interface.
        connection_opts={'IO': 'TCP', 'PORT': int(args[1])}
        server_intf = Mserver.ServerInterface(connection_opts=connection_opts)
        self.errmsg("Going into server mode on port '%s'" % args[1])
        self.debugger.intf.append(server_intf)
        return False

# Demo it
if __name__ == '__main__':
    from trepan.processor.command import mock as Mmock
    d, cp = Mmock.dbg_setup()
    command = ServerCommand(cp)
    if len(sys.argv) > 1:
        command.run([sys.argv[1]])
    pass
