# -*- coding: utf-8 -*-
from import_relative import import_relative

# Our local modules
import_relative('lib', '...', 'pydbg')
Mbase_cmd  = import_relative('base_cmd', top_name='pydbg')
Mfile      = import_relative('lib.file', '...', 'pydbg')
Mbreak     = import_relative('break', '.', 'pydbg')

class ContinueCommand(Mbase_cmd.DebuggerCommand):
    """continue [[file:]lineno | function]

Leave the debugger loop and continue execution. Subsequent entry to
the debugger however may occur via breakpoints or explicit calls, or
exceptions.

If a line position is given, a temporary breakpoint is set at that
position before continuing."""

    category      = 'running'
    execution_set = ['Running']
    min_args      = 0
    max_args      = None
    name_aliases  = ('continue', 'c',)
    need_stack    = True
    short_help    = 'Continue execution of debugged program'

    def run(self, args):
        if len(args) > 1:
            # FIXME: DRY this code. Better is to hook into tbreak. 
            func, filename, lineno, condition = Mbreak.parse_break_cmd(self,
                                                                       args[1:])
            if not Mbreak.set_break(self, func, filename, lineno, condition, 
                                    True, args):
                return False
        self.core.step_events = None # All events
        self.core.step_ignore = -1
        self.continue_running = True # Break out of command read loop
        return True
    pass

if __name__ == '__main__':
    import sys
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    cmd = ContinueCommand(d.core.processor)
    cmd.proc.frame = sys._getframe()
    cmd.proc.setup()
    for c in (['continue', 'wrong', 'number', 'of', 'args'],
              ['c', '5'],
              ['continue', '1+2'],
              ['c', 'foo']):
        d.core.step_ignore = 0
        cmd.continue_running = False
        result = cmd.run(c)
        print 'Run result: %s' % result
        print 'step_ignore %d, continue_running: %s' % (d.core.step_ignore,
                                                        cmd.continue_running,)
        pass
    pass
