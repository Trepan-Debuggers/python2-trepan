# -*- coding: utf-8 -*-
#   Copyright (C) 2009-2010, 2013-2015, 2017 Rocky Bernstein
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
''' Not a command. A stub class used by a command in its 'main' for
demonstrating how the command works.'''

import sys
from trepan.lib import breakpoint, default

class MockIO:
    def readline(self, prompt='', add_to_history=False):
        """
        Reads a line from the user.

        Args:
            self: (todo): write your description
            prompt: (todo): write your description
            add_to_history: (bool): write your description
        """
        print(prompt)
        return 'quit'

    def output(self):
        """
        Output the output of the output.

        Args:
            self: (todo): write your description
        """
        print
    pass

class MockUserInterface:
    def __init__(self):
        """
        Initialize the socket.

        Args:
            self: (todo): write your description
        """
        self.io = MockIO()
        self.output = MockIO()
        return

    def confirm(self, msg, default):
        """
        Confirm a message.

        Args:
            self: (todo): write your description
            msg: (str): write your description
            default: (todo): write your description
        """
        print('** %s' % msg)
        # Ignore the default.
        return True

    def errmsg(self, msg):
        """
        Print an error message

        Args:
            self: (todo): write your description
            msg: (str): write your description
        """
        print('** %s' % msg)
        return

    def finalize(self, last_wishes=None):
        """
        Finalize the stream.

        Args:
            self: (todo): write your description
            last_wishes: (str): write your description
        """
        return

    def msg(self, msg):
        """
        Prints a message

        Args:
            self: (todo): write your description
            msg: (str): write your description
        """
        print(msg)
        return

    def msg_nocr(self, msg):
        """
        Prints a message to the screen.

        Args:
            self: (todo): write your description
            msg: (str): write your description
        """
        sys.stdout.write(msg)
        return
    pass

class MockProcessor:
    def __init__(self, core):
        """
        Initialize a thread.

        Args:
            self: (todo): write your description
            core: (todo): write your description
        """
        self.core         = core
        self.debugger     = core.debugger
        self.continue_running = False
        self.curframe     = None
        self.event2short  = {}
        self.frame        = None
        self.intf         = core.debugger.intf
        self.last_command = None
        self.stack        = []
        return

    def get_int(self, arg, min_value=0, default=1, cmdname=None,
                    at_most=None):
        """
        Return integer value as an integer.

        Args:
            self: (todo): write your description
            arg: (str): write your description
            min_value: (float): write your description
            default: (todo): write your description
            cmdname: (str): write your description
            at_most: (todo): write your description
        """
        return None

    def undefined_cmd(self, cmd):
        """
        Undefined commands.

        Args:
            self: (todo): write your description
            cmd: (str): write your description
        """
        self.intf[-1].errmsg('Undefined mock command: "%s' % cmd)
        return
    pass

# External Egg packages
import tracefilter

class MockDebuggerCore:
    def __init__(self, debugger):
        """
        Initialize a new trace.

        Args:
            self: (todo): write your description
            debugger: (todo): write your description
        """
        self.debugger       = debugger
        self.execution_status = 'Pre-execution'
        self.filename_cache  = {}
        self.ignore_filter  = tracefilter.TraceFilter([])
        self.bpmgr          = breakpoint.BreakpointManager()
        self.processor      = MockProcessor(self)
        self.step_ignore    = -1
        self.stop_frame     = None
        self.last_lineno    = None
        self.last_offset    = None
        self.last_filename  = None
        self.different_line = None
        self.from_ipython   = False
        return

    def set_next(self, frame, step_events=None):
        """
        Sets the next frame.

        Args:
            self: (todo): write your description
            frame: (todo): write your description
            step_events: (todo): write your description
        """
        pass

    """
    Stops.

    Args:
        self: (todo): write your description
    """
    def stop(self): pass

    def canonic(self, filename):
        """
        Returns true if filename is a filename.

        Args:
            self: (todo): write your description
            filename: (str): write your description
        """
        return filename

    def canonic_filename(self, frame):
        """
        Determine whether the frame filename.

        Args:
            self: (todo): write your description
            frame: (todo): write your description
        """
        return frame.f_code.co_filename

    def filename(self, name):
        """
        Returns the filename of a filename.

        Args:
            self: (todo): write your description
            name: (str): write your description
        """
        return name

    def is_running(self):
        """
        Check if the status is running.

        Args:
            self: (todo): write your description
        """
        return 'Running' == self.execution_status

    def get_file_breaks(self, filename):
        """
        Returns a list of filenames for a file.

        Args:
            self: (todo): write your description
            filename: (str): write your description
        """
        return []
    pass

class MockDebugger:
    def __init__(self):
        """
        Initialize the program.

        Args:
            self: (todo): write your description
        """
        self.intf             = [MockUserInterface()]
        self.core             = MockDebuggerCore(self)
        self.settings         = default.DEBUGGER_SETTINGS
        self.from_ipython     = False
        self.orig_sys_argv    = None
        self.program_sys_argv = []
        return

    """
    Stops.

    Args:
        self: (todo): write your description
    """
    def stop(self): pass

    """
    Restart the argv.

    Args:
        self: (todo): write your description
    """
    def restart_argv(self): return []
    pass

def dbg_setup(d = None):
    """
    Setup the dllg_setup command.

    Args:
        d: (str): write your description
    """
    if d is None: d = MockDebugger()
    from trepan.processor import cmdproc
    cp = cmdproc.CommandProcessor(d.core)
    return d, cp
