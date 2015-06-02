Data
====

Examining data.

Disassemble
-----------

*disassemble* [*thing*] [*start-line* [*end-line*]]

With no argument, disassemble the current frame. With an integer
start-line, the disassembly is narrowed to show lines starting at that
line number or later; with an end-line number, disassembly stops when
the next line would be greater than that or the end of the code is hit.

If *start-line* or *end-line is* ``.``, ``+``, or ``-``, the current
line number is used. If instead it starts with a plus or minus prefix to
a number, then the line number is relative to the current frame number.

With a class, method, function, pyc-file, code or string argument
disassemble that.

Examples:
+++++++++

::

       disassemble    # Possibly lots of stuff dissassembled
       disassemble .  # Disassemble lines starting at current stopping point.
       disassemble +                  # Same as above
       disassemble +0                 # Same as above
       disassemble os.path            # Disassemble all of os.path
       disassemble os.path.normcase   # Disaassemble just method os.path.normcase
       disassemble -3  # Disassemble subtracting 3 from the current line number
       disassemble +3  # Disassemble adding 3 from the current line number
       disassemble 3                  # Disassemble starting from line 3
       disassemble 3 10               # Disassemble lines 3 to 10
       disassemble myprog.pyc         # Disassemble file myprog.pyc


Display
-------
**display** [*format*] *expression*

Print value of expression *expression* each time the program stops.
*format* may be used before *expression* and may be one of `/c` for
char, `/x` for hex, `/o` for octal, `/f` for float or `/s` for string.

For now, display expressions are only evaluated when in the same
code as the frame that was in effect when the display expression
was set.  This is a departure from gdb and we may allow for more
flexibility in the future to specify whether this should be the
case or not.

With no argument, evaluate and display all currently requested
auto-display expressions.  Use `undisplay` to cancel display
requests previously made.

Eval
----
**eval** *python-statement*

Run *python-statement* in the context of the current frame.

If no string is given, we run the string from the current source code
about to be run. If the command ends `?` (via an alias) and no string is
given, the following translations occur:

::

   {if|elif} <expr> :  => <expr>
   while <expr> :      => <expr>
   return <expr>       => <expr>
   <var> = <expr>      => <expr>

The above is done via regular expression matching. No fancy parsing is
done, say, to look to see if *expr* is split across a line or whether
var an assignment might have multiple variables on the left-hand side.

Examples:
+++++++++

    eval 1+2  # 3
    eval      # Run current source-code line
    eval?     # but strips off leading 'if', 'while', ..
              # from command

See also:
+++++++++
`set autoeval`, `pr`, `pp` and `examine`.

Set Auto Eval
-------------

*set* *autoeval* [*on*\ \|\ *off*]

Evaluate unrecognized debugger commands.

Often inside the debugger, one would like to be able to run arbitrary
Python commands without having to preface Python expressions with
``print`` or ``eval``. Setting *autoeval* on will cause unrecognized
debugger commands to be *eval*'d as a Python expression.

Note that if this is set, on error the message shown on type a bad
debugger command changes from:

::

      Undefined command: "fdafds". Try "help".

to something more Python-eval-specific such as:

::

      NameError: name 'fdafds' is not defined

One other thing that trips people up is when setting autoeval is that
there are some short debugger commands that sometimes one wants to use
as a variable, such as in an assignment statement. For example:

::

      s = 5

which produces when *autoeval* is on:

::

      Command 'step' can take at most 1 argument(s); got 2.

because by default, ``s`` is an alias for the debugger ``step`` command.
It is possible to remove that alias if this causes constant problem.

Set Auto List
-------------

*set* *autolist* [*on*\ \|\ *off*]

Run the *list* command every time you stop in the debugger. With this,
you will get output like:

::

    -> 1 from subprocess import Popen, PIPE
    (trepan2) next
    (/users/fbicknel/Projects/disk_setup/sqlplus.py:2): <module>
    ** 2 import os
      1     from subprocess import Popen, PIPE
      2  -> import os
      3     import re
      4
      5     class SqlPlusExecutor(object):
      6         def __init__(self, connection_string='/ as sysdba', sid=None):
      7             self.__connection_string = connection_string
      8             self.session = None
      9             self.stdout = None
     10             self.stderr = None
    (trepan2) next
    (/users/fbicknel/Projects/disk_setup/sqlplus.py:3): <module>
    ** 3 import re
      1     from subprocess import Popen, PIPE
      2     import os
      3  -> import re
      4
      5     class SqlPlusExecutor(object):
      6         def __init__(self, connection_string='/ as sysdba', sid=None):
      7             self.__connection_string = connection_string
      8             self.session = None
      9             self.stdout = None
     10             self.stderr = None
    (trepan2)

You may also want to put this this in your debugger startup file. See
[#Startup\_Profile]

Set Different
-------------

Set consecutive stops must be on different file/line positions.

By default, the debugger traces all events possible including line,
exceptions, call and return events. Just this alone may mean that for
any given source line several consecutive stops at a given line may
occur. Independent of this, Python allows one to put several commands in
a single source line of code. When a programmer does this, it might be
because the programmer thinks of the line as one unit.

One of the challenges of debugging is getting the granualarity of
stepping comfortable. Because of the above, stepping all events can
often be too fine-grained and annoying. By setting different on you can
set a more coarse-level of stepping which often still is small enough
that you won't miss anything important.

Note that the 'step' and 'next' debugger commands have '+' and '-'
suffixes if you wan to override this setting on a per-command basis.

See also ``set trace`` to change what events you want to filter.
