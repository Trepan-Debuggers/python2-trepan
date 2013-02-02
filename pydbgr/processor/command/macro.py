# -*- coding: utf-8 -*-
# copyright (c) 2013 rocky bernstein
#   this program is free software: you can redistribute it and/or modify
#   it under the terms of the gnu general public license as published by
#   the free software foundation, either version 3 of the license, or
#   (at your option) any later version.
#
#   this program is distributed in the hope that it will be useful,
#   but without any warranty; without even the implied warranty of
#   merchantability or fitness for a particular purpose.  see the
#   gnu general public license for more details.
#
#   you should have received a copy of the gnu general public license
#   along with this program.  if not, see <http://www.gnu.org/licenses/>.

import os, sys, types

from import_relative import import_relative
Mbase_cmd  = import_relative('base_cmd', top_name='pydbgr')
Mdebugger  = import_relative('debugger', '...', 'pydbgr')

class MacroCommand(Mbase_cmd.DebuggerCommand):
  """**macro** *macro-name* *lambda-object*

Define *macro-name* as a debugger macro. Debugger macros get a list of
arguments. Debugger macros get a list of arguments which you supply
without parenthesis or commas. See below for an example.

The macro (really a Python lambda) should return either a String or an
Array of Strings. The string in both cases are strings of debugger
commands.  If the return is a String, that gets tokenized by a simple
String#split .  Note that macro processing is done right after
splitting on ;; so if the macro returns a string containing ;; this
will not be handled on the string returned.

If instead, Array of Strings is returned, then the first string is
shifted from the array and executed. The remaining strings are pushed
onto the command queue. In contrast to the first string, subsequent
strings can contain other macros, and ;; in those strings will be
split into separate commands.

Here is an example. The below creates a macro called `fin+` which
issues two commands 'finish' followed by 'step':

    macro fin+ lambda: ['finish','step']

If you wanted to parameterize the argument of the `finish` command
you could do that this way:

    macro fin+ lambda levels: ['finish %s' % levels ,'step']

Invoking with:

     fin+ 3

would expand to: `['finish 3', 'step']`

If you were to add another parameter for `step`, the note that the 
invocation might be:

     fin+ 3 2

rather than `fin+(3,2)` or `fin+ 3, 2`.

See also 'info macro'.
  """

  category   = 'support'
  min_args   = 2  # Need at least this many
  max_args   = None
  name       = os.path.basename(__file__).split('.')[0]
  short_help = 'Define a macro'
  
  def run(self, args):
    
    cmd_name = args[1]
    cmd_argstr = self.proc.cmd_argstr[len(cmd_name):].lstrip()
    proc_obj = None
    try:
      proc_obj = eval(cmd_argstr)
    except (SyntaxError, NameError, ValueError):
      self.errmsg("Expecting a Python lambda expression; got %s" % cmd_argstr)
      pass
    if proc_obj:
      if type(proc_obj) == types.FunctionType:
        self.proc.macros[cmd_name] = [proc_obj, cmd_argstr]
        self.msg("Macro \"%s\" defined." % cmd_name)
      else:
        self.errmsg("Expecting a Python lambda expression; got: %s" %
                    cmd_argstr)
        pass
      pass
    return
  pass
        
# Demo it
if __name__ == '__main__':
  Mmock = import_relative('mock')
  dbgr, cmd = Mmock.dbg_setup()
  command = MacroCommand(cmd)
  for cmdline in ["macro foo lambda a,y: x+y",
                  "macro bad2 1+2"]:
    args = cmdline.split()
    cmd_argstr = cmdline[len(args[0]):].lstrip()
    cmd.cmd_argstr = cmd_argstr
    command.run(args)
    pass
  print cmd.macros
  pass
