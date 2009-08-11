# -*- coding: utf-8 -*-
#
#  Copyright (C) 2009 Rocky Bernstein
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
import inspect, os, pyficache

# Our local modules
from import_relative import import_relative

import_relative('lib', '...', 'pydbgr')
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mcmdfns   = import_relative('cmdfns', top_name='pydbgr')
Mfile     = import_relative('file', '...lib', 'pydbgr')
Mmisc     = import_relative('misc', '...', 'pydbgr')

def set_break(cmd_obj, func, filename, lineno, condition, temporary, args):
    if lineno is None:
        part1 = ("I don't understand '%s' as a line number, function name,"
                 % ' '.join(args[1:]))
        msg = Mmisc.wrapped_lines(part1, "or file/module plus line number.",
                                  cmd_obj.settings['width'])
        cmd_obj.errmsg(msg)
        return False
    if filename is None:
        filename = cmd_obj.proc.curframe.f_code.co_filename
        filename = cmd_obj.core.canonic(filename)
        pass
    if func is None:
        ok_linenos = pyficache.trace_line_numbers(filename)
        if lineno not in ok_linenos:
            part1 = ('File %s' % cmd_obj.core.filename(filename))
            msg = Mmisc.wrapped_lines(part1, 
                                      "is not stoppable at line %d." %
                                      lineno, cmd_obj.settings['width'])
            cmd_obj.errmsg(msg)
            return False
        pass
    bp =  cmd_obj.core.bpmgr.add_breakpoint(filename, lineno, temporary, 
                                         condition, func)
    if func:
        cmd_obj.msg('Breakpoint %d set on calling function %s()' 
                 % (bp.number, func.func_name))
        part1 = 'Currently this is line %d of file'  % lineno
        msg = Mmisc.wrapped_lines(part1, cmd_obj.core.filename(filename),
                                  cmd_obj.settings['width'])
    else:
        part1 = ( 'Breakpoint %d set at line %d of file' 
                  % (bp.number, lineno))
        msg = Mmisc.wrapped_lines(part1, cmd_obj.core.filename(filename),
                                  cmd_obj.settings['width'])
        pass
    cmd_obj.msg(msg)
    return True

def parse_break_cmd(cmd_obj, args):
    curframe = cmd_obj.proc.curframe
    if 0 == len(args) or args[0] == 'if':
        filename = cmd_obj.core.canonic(curframe.f_code.co_filename)
        lineno   = curframe.f_lineno
        if 0 == len(args):
            return (None, filename, lineno, None)
        modfunc = None
        condition_pos = 0
    else:
        (modfunc, filename, lineno) = cmd_obj.proc.parse_position(args[0])
        condition_pos = 1
        pass
    if inspect.ismodule(modfunc) and lineno is None and len(args) > 1:
        val = cmd_obj.proc.get_an_int(args[1], 
                                   'Line number expected, got %s.' % 
                                   args[1])
        if val is None: return (None, None, None, None)
        lineno = val
        condition_pos = 2
        pass
    if len(args) > condition_pos and 'if' == args[condition_pos]:
        condition = ' '.join(args[condition_pos+1:])
    else:
        condition = None
        pass
    if inspect.isfunction(modfunc):
        func = modfunc
    else:
        func = None
    return (func, filename, lineno, condition)

class BreakCommand(Mbase_cmd.DebuggerCommand):
    """break [LOCATION] [if CONDITION]]

With a line number argument, set a break there in the current file.
With a function name, set a break at first executable line of that
function.  Without argument, set a breakpoint at current location.  If
a second argument is "if", subsequent arguments given an expression
which must evaluate to true before the breakpoint is honored.

The location line number may be prefixed with a filename or module
name and a colon. Files is searched for using sys.path, adnd the .py
suffix may be omitted in the file name.

Examples:
   break              # Break where we are current stopped at
   break if i < j     # Break at current line if i < j
   break 10           # Break on line 10 of the file we are currently stopped at
   break os.path.join # Break in function os.path.join
   break os.path:45   # Break on line 45 of os.path
   break myfile:5 if i < j # Same as above but only if i < j
   break myfile.py:45 # Break on line 45 of myfile.py
   break myfile:45    # Same as above.
"""

    aliases       = ('b',)
    category      = 'breakpoints'
    min_args      = 0
    max_args      = None
    name          = os.path.basename(__file__).split('.')[0]
    need_stack    = True
    short_help    = 'Set breakpoint at specified line or function'

    def run(self, args):
        func, filename, lineno, condition = parse_break_cmd(self, args[1:])
        set_break(self, func, filename, lineno, condition, False, args)
        return 

if __name__ == '__main__':
    import sys
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    command = BreakCommand(d.core.processor)
    command.proc.frame = sys._getframe()
    command.proc.setup()

    print parse_break_cmd(command, [])
    print parse_break_cmd(command, ['10'])
    print parse_break_cmd(command, [__file__ + ':10'])
    def foo():
        return 'bar'
    print parse_break_cmd(command, ['foo'])
    print parse_break_cmd(command, ['os.path'])
    print parse_break_cmd(command, ['os.path', '5+1'])
    print parse_break_cmd(command, ['os.path.join'])
    print parse_break_cmd(command, ['if', 'True'])
    print parse_break_cmd(command, ['foo', 'if', 'True'])
    print parse_break_cmd(command, ['os.path:10', 'if', 'True'])
    command.run(['break'])
    command.run(['break', 'command.run'])
    command.run(['break', '10'])
    command.run(['break', __file__ + ':10'])
    command.run(['break', 'foo'])
    pass
