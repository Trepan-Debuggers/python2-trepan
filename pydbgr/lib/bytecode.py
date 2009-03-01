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

from opcode import *
import dis
import re

def op_at_code_loc(code, loc):
    try:
        op = ord(code[loc])
    except IndexError:
        return 'got IndexError'
    return opname[op]

def op_at_frame(frame, loc=None):
    code = frame.f_code.co_code
    if loc is None: loc = frame.f_lasti
    return op_at_code_loc(code, loc)

def next_opcode(code, offset):
    '''Return the next opcode and offset as a tuple. Tuple (-100,
    -1000) is returned when reaching the end.'''
    n = len(code)
    while offset < n:
        c = code[offset]
        op = ord(c)
        offset += 1
        if op >= HAVE_ARGUMENT:
            offset += 2
            pass
        yield op, offset
        pass
    yield -100, -1000
    pass

def next_linestart(co, offset, count=1):
    linestarts = dict(dis.findlinestarts(co))
    code = co.co_code
    n = len(code)
    contains_cond_jump = False
    for op, offset in next_opcode(code, offset):
        if offset in linestarts: 
            count -= 1
            if 0 == count:
                return linestarts[offset]
            pass
        pass
    return -1000

# FIXME: break out into a code iterator.
def stmt_contains_make_function(co, lineno):
    linestarts = dict(dis.findlinestarts(co))
    code = co.co_code
    found_start = False
    for offset, start_line in linestarts.items():
        if start_line == lineno: 
            found_start = True
            break
        pass
    if not found_start: 
        return False
    for op, offset in next_opcode(code, offset):
        if -1000 == offset or linestarts.get(offset): return False
        opcode = opname[op]
        # print opcode
        if 'MAKE_FUNCTION' == opcode:
            return True
        pass
    return False

# A pattern for a def header seems to be used a couple of times.
_re_def_str = r'^\s*def\s'
_re_def = re.compile(_re_def_str)
def is_def_stmt(line, frame):
    """Return True if we are looking at a def statement"""
    # Should really also check that operand is a code object
    return _re_def.match(line) and op_at_frame(frame)=='LOAD_CONST' \
        and stmt_contains_make_function(frame.f_code, frame.f_lineno)

# Demo stuff above
if __name__=='__main__':
    import inspect
    def sqr(x):
        return x * x
    frame = inspect.currentframe()
    co = frame.f_code
    lineno = frame.f_lineno
    print 'contains MAKE_FUNCTION', stmt_contains_make_function(co, lineno-4)
    print 'contains MAKE_FUNCTION', stmt_contains_make_function(co, lineno)

    print "op at frame: ", op_at_frame(frame)
    print "op at frame, position 2", op_at_frame(frame, 2)
    print "def statement: x=5?: ", is_def_stmt('x=5', frame)
    # Not a "def" statement because frame is wrong spot
    print is_def_stmt('def foo():', frame)

    pass
