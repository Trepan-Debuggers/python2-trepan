# -*- coding: utf-8 -*-
#
#  Copyright (C) 2009, 2010, 2015, 2017 Rocky Bernstein
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

import inspect, pyficache
import os.path as osp

from trepan.lib import stack as Mstack
from trepan import misc as Mmisc
from trepan.processor.parse.semantics import build_bp_expr
from trepan.processor.parse.parser import LocationError
from trepan.processor.parse.scanner import ScannerError

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
        if not ok_linenos or lineno not in ok_linenos:
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


INVALID_PARSE_BREAK = (None, None, None, None)
def parse_break_cmd(proc, args):
    curframe = proc.curframe
    if proc.current_command is None:
        proc.errmsg("Don't have program source text")
        return INVALID_PARSE_BREAK

    text = proc.current_command[len(args[0])+1:]
    if len(args) > 1 and args[1] == 'if':
        location = '.'
        condition = text[text.find('if ')+3:]
    elif text == '':
        location = '.'
        condition  = None
    else:
        try:
            bp_expr   = build_bp_expr(text)
        except LocationError as e:
            proc.errmsg("Error in parsing breakpoint expression at or around:")
            proc.errmsg(e.text)
            proc.errmsg(e.text_cursor)
            return INVALID_PARSE_BREAK
        except ScannerError as e:
            proc.errmsg("Lexical error in parsing breakpoint expression at or around:")
            proc.errmsg(e.text)
            proc.errmsg(e.text_cursor)
            return INVALID_PARSE_BREAK

        location  = bp_expr.location
        condition = bp_expr.condition
        lineno    = bp_expr.location.line_number

        # Validate arguments that can't be done in parsing
        if proc.curframe:
            g = curframe.f_globals
            l = curframe.f_locals
        else:
            g = globals()
            l = locals()
            pass

    if location == '.':
        filename = Mstack.frame2file(proc.core, curframe, canonic=False)
        lineno   = curframe.f_lineno
        modfunc  = None
    elif location.method:
        filename = lineno = None
        msg = ('Object %s is not known yet as a function, ' % location.method)
        try:
            modfunc = eval(location.method, g, l)
        except:
            proc.errmsg(msg)
            return INVALID_PARSE_BREAK

        try:
            # Check if the converted string is a function
            if inspect.isfunction(modfunc):
                pass
            else:
                proc.errmsg(msg)
                return INVALID_PARSE_BREAK
        except:
            proc.errmsg(msg)
            return INVALID_PARSE_BREAK
        filename = proc.core.canonic(modfunc.func_code.co_filename)
        lineno   = modfunc.func_code.co_firstlineno
    elif location.path:
        filename = proc.core.canonic(location.path)
        lineno  =  location.line_number
        modfunc  = None
        if not osp.isfile(filename):
            # See if argument is a module
            try:
                modfunc = eval(location.path, g, l)
            except:
                proc.errmsg(msg)
                return INVALID_PARSE_BREAK
            pass
            if inspect.ismodule(modfunc):
                filename = pyficache.pyc2py(modfunc.__file__)
                filename = proc.core.canonic(filename)
                # FIXME: ???
                # We could pick out a line number, but we've already
                # have passed at and won't it it again
                return modfunc, filename, lineno, condition

            proc.errmsg("%s is not known as a file" % location.path)
            return INVALID_PARSE_BREAK
        maxline = pyficache.maxline(filename)
        if lineno > maxline:
            proc.errmsg("%s has %d lines; requested line %d" % (location.path, lineno))
            return INVALID_PARSE_BREAK
    elif location.line_number:
        filename = Mstack.frame2file(proc.core, curframe, canonic=False)
        lineno   = location.line_number
        modfunc  = None

    return modfunc, filename, lineno, condition


# # Demo it
# if __name__=='__main__':
#     from trepan.processor.command import mock as Mmock
#     from trepan.processor.cmdproc import CommandProcessor
#     import sys
#     d = Mmock.MockDebugger()
#     cmdproc = CommandProcessor(d.core)
#     # print '-' * 10
#     # print_source_line(sys.stdout.write, 100, 'source_line_test.py')
#     # print '-' * 10
#     cmdproc.frame = sys._getframe()
#     cmdproc.setup()
#     for cmd in (
#             # "break '''c:\\tmp\\foo.bat''':1",
#             'break """/Users/My Documents/foo.py""":2',
#             # "break",
#             # "break 10",
#             # "break if True",
#             # "break cmdproc.py:5",
#             # "break set_break()",
#             # "break cmdproc.setup()",
#             # "break cmdproc.setup()",
#             ):
#         args = cmd.split(' ')
#         cmdproc.current_command = cmd
#         print(parse_break_cmd(cmdproc, args))
#     pass
