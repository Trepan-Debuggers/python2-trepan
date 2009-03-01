# -*- coding: utf-8 -*-
import sys
from import_relative import *

# Our local modules
base_cmd  = import_relative('base_cmd')
Mdebugger = import_relative('debugger', '...')
from cmdfns import *

class DExecCommand(base_cmd.DebuggerCommand):

    category      = 'support'
    min_args      = 0
    max_args      = None
    name_aliases  = ('dexec',)
    need_stack    = True

    def run(self, args):
        """dcall fn arg1 arg2 - debug call
"""
        cmd = ' '.join(args[1:])
        fr = self.proc.curframe
        sys.call_tracing(eval, (cmd, fr.f_globals, fr.f_locals))
        return False

# Demo it
if __name__ == '__main__':
    mock = import_relative('mock')
    d, cp = mock.dbg_setup()
    command = DExecCommand(cp)
    def trace_me(a):
        a += 1
        print a
        return
    command.run(['dexec', 'trace_me', '5'])
    pass
