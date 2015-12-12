# -*- coding: utf-8 -*-
#   Copyright (C) 2015 Rocky Bernstein <rocky@gnu.org>
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


# Our local modules
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan.lib import complete as Mcomplete
from trepan.processor import frame as Mframe


class InfoFrame(Mbase_subcmd.DebuggerSubcommand):
    """**info frame** [-c] [ *frame-number* ]

Show the detailed information *frame-number* or the current frame if
*frame-number* is not specified.

Specific information includes:

* the frame number

* the source-code line number that this frame is stopped in

* the last instruction executed; -1 if the program are before the first
instruction

* a function that tracing this frame or `None`

* Whether the frame is in restricted execution

If `-c` is given we show some information on the associated Python code object
for this frame.

See also:
---------

`info locals`, `info globals`, `info args`"""

    min_abbrev = 2
    max_args = 2
    need_stack = True
    short_help = '''Show detailed info about the current frame'''

    def complete(self, prefix):
        proc_obj = self.proc
        low, high = Mframe.frame_low_high(proc_obj, None)
        ary = [str(low+i) for i in range(high-low+1)]
        # FIXME: add in Thread names
        return Mcomplete.complete_token(ary, prefix)

    def run(self, args):
        proc = self.proc
        frame = proc.curframe
        if not frame:
            self.errmsg("No frame selected.")
            return False

        show_code = False
        if len(args) >= 1 and args[0] == '-c':
            args.pop(0)
            show_code = True

        if len(args) == 1:
            frame_num = self.proc.get_an_int(args[0],
                                         ("The 'frame' command requires a" +
                                          " frame number. Got: %s") %
                                         args[0])
            if frame_num is None: return False

            i_stack = len(proc.stack)
            if frame_num < -i_stack or frame_num > i_stack-1:
                self.errmsg(('Frame number has to be in the range %d to %d.' +
                             ' Got: %d (%s).') % (-i_stack, i_stack-1,
                                                  frame_num, args[0]))
                return False
            frame = proc.stack[frame_num][0]
        else:
            frame_num = len(proc.stack)-1-proc.curindex

        self.section('Frame %d' % frame_num)
        self.msg('  line number: %d' % frame.f_lineno)
        self.msg('  last instruction: %d' % frame.f_lasti)
        if frame.f_exc_type:
            self.msg('  exception type: %s' % frame.f_exc_type)
            self.msg('  exception value: %s'% frame.f_exc_value)
        self.msg('  tracing function: %s' % frame.f_trace)
        if hasattr(frame, 'f_restricted'):
            self.msg('  restricted execution: %s' % frame.f_restricted)

        # FIXME: we have an info code that has everything?
        if show_code:
            code = frame.f_code
            self.section('Associated code')
            self.msg("  name: %s" % code.co_name)
            self.msg('  number of arguments: %d' % code.co_argcount)
            self.msg('  number of locals: %d' % code.co_nlocals)
            self.msg("  stacksize %s" % code.co_stacksize)
            self.msg("  first line number: %s" % code.co_firstlineno)
            self.msg("  is%s optimized" % ("" if (code.co_flags & 1) == 1 else " not"))
            self.msg("  has%s newlocals" % ("" if (code.co_flags & 2) == 1 else " no"))
            self.msg("  has%s *args" % ("" if (code.co_flags & 4) == 1 else " no"))
            self.msg("  has%s **args" % ("" if (code.co_flags & 8) == 1 else " no"))
            print(code.co_varnames)

        return False
    pass

if __name__ == '__main__':
    from trepan.processor.command import mock, info as Minfo
    d, cp = mock.dbg_setup()
    i = Minfo.InfoCommand(cp)
    sub = InfoFrame(i)
    import inspect
    cp.curframe = inspect.currentframe()
    sub.run([])
