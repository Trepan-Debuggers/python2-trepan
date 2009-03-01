# -*- coding: utf-8 -*-
import inspect
from import_relative import *


# Our local modules
base_cmd  = import_relative('base_cmd')
Mdebugger = import_relative('debugger', '...')
from cmdfns import *

class FTraceCommand(base_cmd.DebuggerCommand):
        """ftrace fn """

    category      = 'support'
    min_args      = 1
    max_args      = 1
    name_aliases  = ('ftrace',)
    need_stack    = True
    short_help    = 'set debugging on a function or method'

    def run(self, args):
        fn = args[0]
        if not eval("inspect.isfunction(%s)" % fn):
            self.errmsg("ftrace parameter %s needs to be a function" % fn)
            return False
        code = eval("%s.func_code" % fn)
        

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
