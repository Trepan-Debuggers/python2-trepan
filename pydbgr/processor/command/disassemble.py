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

import types
from dis import distb, findlabels, findlinestarts
from opcode import cmp_op, hasconst, hascompare, hasfree, hasname, hasjrel, \
    haslocal, opname, EXTENDED_ARG, HAVE_ARGUMENT

# Modified from dis. Changed output to use msg and msg_nocr.
# Added first_line and last_line parameters
def dis(msg, msg_nocr, errmsg, x=None, start_line=-1, end_line=None,
        relative_pos = False):
    """Disassemble classes, methods, functions, or code.

    With no argument, disassemble the last traceback.

    """
    if x is None:
        distb()
        return
    if type(x) is types.InstanceType:
        x = x.__class__
    if hasattr(x, 'im_func'):
        msg("Disassembly of %s: " % x)
        x = x.im_func
    if hasattr(x, 'func_code'):
        msg("Disassembly of %s: " % x)
        x = x.func_code
    elif hasattr(x, 'f_code'):
        msg("Disassembly of %s: " % x)
        x = x.f_code
        pass
    if hasattr(x, '__dict__'):
        items = x.__dict__.items()
        items.sort()
        for name, x1 in items:
            if type(x1) in (types.MethodType,
                            types.FunctionType,
                            types.CodeType,
                            types.ClassType):
                try:
                    dis(msg, msg_nocr, errmsg, x1, 
                        start_line=start_line, end_line=end_line, 
                        relative_pos = relative_pos)
                    msg("")
                except TypeError, msg:
                    errmsg("Sorry:", msg)
    elif hasattr(x, 'co_code'):
        disassemble(msg, msg_nocr, x, start_line=start_line, end_line=end_line,
                    relative_pos = relative_pos)
    elif isinstance(x, str):
        disassemble_string(msg, msg_nocr, x,)
    else:
       errmsg("Don't know how to disassemble %s objects." % 
              type(x).__name__)
    return

def disassemble(msg, msg_nocr, co, lasti=-1, start_line=-1, end_line=None,
                relative_pos=False):
    """Disassemble a code object."""
    disassemble_string(msg, msg_nocr, co.co_code, lasti, co.co_firstlineno,
                       start_line, end_line, relative_pos,
                       co.co_varnames, co.co_names, co.co_consts,
                       co.co_cellvars, co.co_freevars,
                       dict(findlinestarts(co)))
    return

def disassemble_string(orig_msg, orig_msg_nocr, code, lasti=-1, cur_line=0,
                       start_line=-1, end_line=None, relative_pos=False,
                       varnames=(), names=(), consts=(), cellvars=(),
                       freevars=(), linestarts={}):
    """Disassemble byte string of code. If end_line is negative
    it counts the number of statement linestarts to use."""
    statement_count = 10000
    if end_line is None:
        end_line = 10000
    elif relative_pos:
        end_line += start_line -1
        pass
    labels = findlabels(code)
    n = len(code)
    i = 0
    extended_arg = 0
    free = None
    null_print = lambda x: None
    if start_line > cur_line:
        msg_nocr = null_print
        msg = null_print
    else:
        msg_nocr = orig_msg_nocr
        msg = orig_msg
        pass
    while i < n and statement_count >= 0:
        c = code[i]
        op = ord(c)
        if i in linestarts:
            if i > 0:
                msg("")
            cur_line = linestarts[i]
            if start_line and start_line > cur_line:
                msg_nocr = null_print
                msg = null_print
            else:
                statement_count -= 1
                msg_nocr = orig_msg_nocr
                msg = orig_msg
                pass
            if cur_line > end_line: break
            msg_nocr("%3d" % cur_line)
        else:
            msg_nocr('   ')

        if i == lasti: msg_nocr('-->')
        else: msg_nocr('   ')
        if i in labels: msg_nocr('>>')
        else: msg_nocr('  ')
        msg_nocr(repr(i).rjust(4))
        msg_nocr(' ')
        msg_nocr(opname[op].ljust(20))
        i += 1
        if op >= HAVE_ARGUMENT:
            oparg = ord(code[i]) + ord(code[i+1])*256 + extended_arg
            extended_arg = 0
            i += 2
            if op == EXTENDED_ARG:
                extended_arg = oparg*65536L
            msg_nocr(repr(oparg).rjust(5))
            msg_nocr(' ')
            if op in hasconst:
                msg_nocr('(' + repr(consts[oparg]) + ')')
            elif op in hasname:
                msg_nocr('(' + names[oparg] + ')')
            elif op in hasjrel:
                msg_nocr('(to ' + repr(i + oparg) + ')')
            elif op in haslocal:
                msg_nocr('(' + varnames[oparg] + ')')
            elif op in hascompare:
                msg_nocr('(' + cmp_op[oparg] + ')')
            elif op in hasfree:
                if free is None:
                    free = cellvars + freevars
                msg_nocr('(' + free[oparg] + ')')
        msg("")
    return

from import_relative import import_relative

# Our local modules
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mcmdfns   = import_relative('cmdfns', top_name='pydbgr')

class DisassembleCommand(Mbase_cmd.DebuggerCommand):

    category      = 'data'
    min_args      = 0
    max_args      = 2
    name_aliases  = ('disassemble','disas') # Note: we will have disable
    need_stack    = True
    short_help    = 'Disassemble Python bytecode'

    def run(self, args):
        """disassemble [obj-or-class] [[+|-]start-line [[+|-]end-line]]

With no argument, disassemble the current frame.  With a start-line
integer, the disassembly is narrowed to show lines starting at that
line number or later; with an end-line number, disassembly stops
when the next line would be greater than that or the end of the code
is hit. If start-line or end-line has a plus or minus prefix, then the
line number is relative to the current frame number.

With a class, method, function, code or string argument disassemble
that."""

        start_line = end_line = None
        relative_pos = False
        try:
            if len(args) > 1:
                if args[1] in ['+', '-']: 
                    start_line = self.proc.curframe.f_lineno
                    relative_pos = True
                else:
                    start_line = int(args[1])
                    if args[1][0:1] in ['+', '-']: 
                        relative_pos = True
                        start_line += self.proc.curframe.f_lineno
                        pass
                    pass

                if len(args) == 3:
                    try:
                        end_line = Mcmdfns.get_int(self.errmsg, args[2], 
                                                   cmdname="disassemble")
                    except ValueError:
                        return False
                    pass
                elif len(args) > 3:
                    self.errmsg("Expecting 1-2 line parameters, got %d" %
                                len(args)-1)
                    return False
            if not self.proc.curframe:
                self.errmsg("No frame selected.")
                return False
            dis(self.msg, self.msg_nocr, self.errmsg, 
                self.proc.curframe, 
                start_line=start_line, end_line=end_line, 
                relative_pos=relative_pos)
        except ValueError:
            try:
                if len(args) > 2:
                    try:
                        start_line = Mcmdfns.get_int(self.errmsg, args[2],
                                                     cmdname="disassemble")
                        if args[2][0:1] in ['+', '-']: 
                            relative_pos = True
                            start_line += self.proc.curframe.f_lineno
                            pass
                        if len(args) == 4:
                            end_line = self.get_int(self.errmsg, args[3],
                                                    cmdname="disassemble")
                        elif len(args) > 4:
                            self.errmsg("Expecting 0-3 parameters, got %d" %
                                        len(args)-1)
                            return False
                    except ValueError:
                        return False
                    pass

                if hasattr(self.proc, 'curframe') and self.proc.curframe:
                    obj=Mcmdfns.get_val(self.proc.curframe, self.errmsg, 
                                        args[1])
                else:
                    obj=eval(args[1])
                    pass
                dis(self.msg, self.msg_nocr, self.errmsg, obj, 
                    start_line=start_line, end_line=end_line, 
                    relative_pos=relative_pos)
            except NameError:
                self.errmsg("Object '%s' is not something we can disassemble"
                            % args[1])
        return False

        """exit [exitcode] - hard exit of the debugged program.  

The program being debugged is exited via sys.exit(). If a return code
is given that is the return code passed to sys.exit() - presumably the
return code that will be passed back to the OS."""

        self.core.stop()
        self.core.execution_status = 'Exit command'
        if len(args) <= 1:
            exitcode = 0
        else:
            try:
                exitcode = self.get_pos_int(self.errmsg, args[1], default=0,
                                            cmdname='disassemble')
            except ValueError:
                return False
            pass
        # FIXME: allow setting a return code.
        import sys
        sys.exit(exitcode)
        # Not reached
        return True

# Demo it
if __name__ == '__main__':
    mock = import_relative('mock')
    d, cp = mock.dbg_setup()
    import inspect
    me = cp.errmsg  # So we can pass that into a command
    cp.curframe = inspect.currentframe()
    dis(cp.msg, cp.msg_nocr, cp.errmsg, cp.curframe,
        start_line=10, end_line=40)
    dis(cp.msg, cp.msg_nocr, cp.errmsg, cp)
    command = DisassembleCommand(cp)
    print '-' * 20
    command.run(['disassemble'])
    print '-' * 20
    command.run(['disassemble', 'me'])
    print '-' * 20
    command.run(['disassemble', '+0', '2'])
    print '-' * 20
    command.run(['disassemble', '+', '1'])
    print '-' * 20
    command.run(['disassemble', '-', '1'])
    print '-' * 20
    pass
