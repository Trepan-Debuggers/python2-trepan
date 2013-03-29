# -*- coding: utf-8 -*-
#   Copyright (C) 2009-2010, 2013 Rocky Bernstein <rocky@gnu.org>
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
"""Interface when communicating with the user in the same process as
    the debugged program."""
import atexit, os, readline

# Our local modules
from import_relative import import_relative
Mfile      = import_relative('lib.file',   '...pydbgr')
Minterface = import_relative('interface',  '...pydbgr')
Minput     = import_relative('io.input', '...pydbgr')
Moutput    = import_relative('io.output', '...pydbgr')

histfile = os.path.expanduser('~/.pydbgr_hist')

DEFAULT_USER_SETTINGS = {
    'histfile'     : histfile, # Where do we save the history?
    'hist_save'     : True,    # Save debugger history?

}


class UserInterface(Minterface.DebuggerInterface):
    """Interface when communicating with the user in the same
    process as the debugged program."""

    FILE_HISTORY='.pydbgr_hist'

    def __init__(self, inp=None, out=None, opts=DEFAULT_USER_SETTINGS):
        atexit.register(self.finalize)
        self.interactive = True # Or at least so we think initially
        self.input       = inp or Minput.DebuggerUserInput()
        self.output      = out or Moutput.DebuggerUserOutput()
        self.history_file = None

        if 'complete' in opts and hasattr(readline, 'set_completer'):
            readline.set_completer = opts['complete']
            pass

        if 'histfile' in opts and hasattr(readline, 'read_history_file'):
            self.history_file = opts['histfile']
            if Mfile.readable(self.history_file):
                readline.read_history_file(self.history_file)
            atexit.register(readline.write_history_file, self.history_file)
            pass

        return

    def close(self):
        """ Closes both input and output """
        self.input.close()
        self.output.close()
        return

    def confirm(self, prompt, default):
        """ Called when a dangerous action is about to be done, to make
        sure it's okay. Expect a yes/no answer to `prompt' which is printed,
        suffixed with a question mark and the default value.  The user
        response converted to a boolean is returned."""
        if default:
            prompt += '? (Y or n) '
        else:
            prompt += '? (N or y) '
            pass
        while True:
            try:
                reply = self.readline(prompt)
                reply = reply.strip().lower()
            except EOFError:
                return default
            if reply in ('y', 'yes'):
                return True
            elif reply in ('n', 'no'):
                return False
            else:
                self.msg("Please answer y or n.")
                pass
            pass
        return default

    def errmsg(self, msg, prefix="** "):
        """Common routine for reporting debugger error messages.
           """
        return self.msg("%s%s" %(prefix, msg))

    def finalize(self, last_wishes=None):
        # print exit annotation
        self.close()
        return

    def read_command(self, prompt=''):
        line = self.readline(prompt)
        if hasattr(self.input, 'add_history'):
            self.input.add_history(line)
            pass
        return line

    def readline(self, prompt=''):
        if (hasattr(self.input, 'use_raw')
            and not self.input.use_raw
            and prompt and len(prompt) > 0):
            self.output.write(prompt)
            self.output.flush()
            pass
        return self.input.readline(prompt=prompt)
    pass

# Demo
if __name__=='__main__':
    intf = UserInterface()
    intf.errmsg("Houston, we have a problem here!")
    import sys
    if len(sys.argv) > 1:
        try:
            line = intf.readline("Type something: ")
        except EOFError:
            print("No input EOF: ")
        else:
            print("You typed: %s" % line)
            pass
        line = intf.confirm("Are you sure", False)
        print("You typed: %s" % line)
        line = intf.confirm("Are you not sure", True)
        print("You typed: %s" % line)
        pass
    pass
