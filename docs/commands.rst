Command Reference
*****************

Following *gdb*, we classify commands into the following categories:

* breakpoints -- Making program stop at certain points
* data -- Examining data
* files -- Specifying and examining files
* running -- Running the program
* stack -- Examining the stack
* status -- Status inquiries
* support -- Support facilities


.. toctree::
   :maxdepth: 2

Breakpoints
===========

Break
-----
**break** [*location*] [if *condition*]]

With a line number argument, set a break there in the current file.
With a function name, set a break at first executable line of that
function.  Without argument, set a breakpoint at current location.  If
a second argument is `if`, subsequent arguments given an expression
which must evaluate to true before the breakpoint is honored.

The location line number may be prefixed with a filename or module
name and a colon. Files is searched for using *sys.path*, and the `.py`
suffix may be omitted in the file name.

Examples:
+++++++++

::

   break              # Break where we are current stopped at
   break if i < j     # Break at current line if i < j
   break 10           # Break on line 10 of the file we are
                      # currently stopped at
   break os.path.join # Break in function os.path.join
   break os.path:45   # Break on line 45 of os.path
   break myfile:5 if i < j # Same as above but only if i < j
   break myfile.py:45 # Break on line 45 of myfile.py
   break myfile:45    # Same as above.

See also:
+++++++++

`tbreak`.

Condition
---------

**condition** *bp_number* *condition*

*bp_number* is a breakpoint number. *condition* is an expression which
must evaluate to *True* before the breakpoint is honored.  If *condition*
is absent, any existing condition is removed; i.e., the breakpoint is
made unconditional.

Examples:
+++++++++

::

   condition 5 x > 10  # Breakpoint 5 now has condition x > 10
   condition 5         # Remove above condition

See also:
+++++++++

`break`, `tbreak`.


Data
====

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

Files
=====

List (show me the code!)
------------------------

The list command will show you your source code::

::

        (trepan2) list 2
          1     #!/usr/bin/python
          2     """Greatest Common Divisor
          3
          4     Some characterstics of this program used for testing check_args() does
          5     not have a 'return' statement.
          6
          7     check_args() raises an uncaught exception when given the wrong number
          8     of parameters.
          9
         10  -> """
        (trepan2) list # keep going
         11     import sys
         12
         13     def check_args():
         14         if len(sys.argv) != 3:
         15             # Rather than use sys.exit let's just raise an error
         16             raise Exception, "Need to give two numbers"
         17         for i in range(2):
         18             try:
         19                 sys.argv[i+1] = int(sys.argv[i+1])
         20             except ValueError:
        (trepan2) import os.path  # Assumes set autoeval on
        (trepan2) list os.path 1 11
          1     """Common operations on Posix pathnames.
          2
          3     Instead of importing this module directly, import os and refer to
          4     this module as os.path.  The "os.path" name is an alias for this
          5     module on Posix systems; on other systems (e.g. Mac, Windows),
          6     os.path provides the same operations in a manner specific to that
          7     platform, and is an alias to another module (e.g. macpath, ntpath).
          8
          9     Some of this can actually be useful on non-Posix systems too, e.g.
         10     for manipulation of the pathname component of URLs.
         11     """
        (trepan2) list os.path.join
         51
         52     # Join pathnames.
         53     # Ignore the previous parts if a part is absolute.
         54     # Insert a '/' unless the first part is empty or already ends in '/'.
         55
         56     def join(a, *p):
         57         """Join two or more pathname components, inserting '/' as needed"""
         58         path = a
         59         for b in p:
         60             if b.startswith('/'):
        (trepan2) remember_this_line=17
        (trepan2) list remember_this_line
         12
         13     def check_args():
         14         if len(sys.argv) != 3:
         15             # Rather than use sys.exit let's just raise an error
         16             raise Exception, "Need to give two numbers"
         17         for i in range(2):
         18             try:
         19                 sys.argv[i+1] = int(sys.argv[i+1])
         20             except ValueError:
         21                 print "** Expecting an integer, got: %s" % repr(sys.argv[i])
         (trepan2)

There are many more options and possibilities so check out ``help list``
for details. If you are not using *trepan2* via some sort of front-end
program (e.g. I generally use `my GNU Emacs
front-end <http://github.com/rocky/emacs-dbgr>`__. Also see
[#Set\_Auto\_List] below.

Running
=======

Step, Next, Finish, Skip, Retval
--------------------------------

Here's a sample session using these commands:

.. code:: python

        (trepan2) set basename  # Short filenames in display
        (trepan2) set trace  # Show the events
        (trepan2) step 4
        line - gcd.py:13
        line - gcd.py:26
        line - gcd.py:40
        line - gcd.py:41
        (gcd.py:41): <module>
        ** 41     check_args()
        (trepan2) s # 's' is an abbreviation for step
        call - gcd.py:13
        (gcd.py:13): check_args
        -> 13 def check_args():
        (trepan2) step<   # Step until the next return
        line - gcd.py:14
        line - gcd.py:17
        line - gcd.py:18
        line - gcd.py:19
        line - gcd.py:17
        line - gcd.py:18
        line - gcd.py:19
        line - gcd.py:17
        return - gcd.py:17
        (gcd.py:17): check_args
        <- 17     for i in range(2):
        (trepan2) set trace off # That's enough tracing
        (trepan2) next  # like step but skips over function calls
        (gcd.py:43): <module>
        ** 43     (a, b) = sys.argv[1:3]
        (trepan2) # A carriage-return or empty command runs the last step/next
        (gcd.py:44): <module>
        ** 44     print "The GCD of %d and %d is %d" % (a, b, gcd(a, b))
        (trepan2) s<  # step until the next call
        (gcd.py:26): gcd
        -> 26 def gcd(a,b):
        (trepan2) finish  # run until return of *this* function; compare with s<
        (gcd.py:38): gcd
        <- 38     return gcd(b-a, a)
        (trepan2) retval  # show the return value
          1
        (trepan2)

Stack
======

Status
=======

Support
=======

Alias
-----

**alias** *alias-name* *debugger-command*

Add alias *alias-name* for a debugger command *debugger-comand*.

Add an alias when you want to use a command abbreviation for a command
that would otherwise be ambigous. For example, by default we make ``s``
be an alias of ``step`` to force it to be used. Without the alias, ``s``
might be ``step``, ``show``, or ``set`` among others

**Example:**

::

        alias cat list   # "cat myprog.py" is the same as "list myprog.py"
        alias s   step   # "s" is now an alias for "step".
                         # The above example is done by default.

See also ``unalias`` and ``show alias``.

Help
----

The help system has been reworked from *pydb* and *pdb* and it is more
extensive now. Play around with it. Starting with a plain help

.. code:: console

      (trepan2) help
      Classes of commands:

      breakpoints   ** Making the program stop at certain points
      data          ** Examining data
      ...

      (trepan2) help breakpoints
      List of commands:

      break         ** Set breakpoint at specified line or function
      condition     ** Specify breakpoint number N ...
      ...
      (trepan2) help *
      List of all debugger commands:
        break        enable   ipython  python   source
        condition    examine  jump     quit     step
        ...

You can set the line width to use in displaying the help output using
the command: ``set width``. To see the current line width, initially
taken from the *COLUMNS* environment variable, type: ``show width``.

Macro
-----

*macro* *macro-name* *lambda-object*

Define *macro-name* as a debugger macro. Debugger macros get a list of
arguments which you supply without parenthesis or commas. See below for
an example.

The macro (really a Python lambda) should return either a String or an
List of Strings. The string in both cases is a debugger command. Each
string gets tokenized by a simple split() . Note that macro processing
is done right after splitting on ``;;``. As a result, if the macro
returns a string containing ``;;`` this will not be interpreted as
separating debugger commands.

If a list of strings is returned, then the first string is shifted from
the list and executed. The remaining strings are pushed onto the command
queue. In contrast to the first string, subsequent strings can contain
other macros. ``;;`` in those strings will be split into separate
commands.

Here is an trivial example. The below creates a macro called ``l=``
which is the same thing as ``list .``:

::

        macro l= lambda: 'list .'

A simple text to text substitution of one command was all that was
needed here. But usually you will want to run several commands. So those
have to be wrapped up into a list.

The below creates a macro called ``fin+`` which issues two commands
``finish`` followed by ``step``:

::

        macro fin+ lambda: ['finish','step']

If you wanted to parameterize the argument of the ``finish`` command you
could do that this way:

::

        macro fin+ lambda levels: ['finish %s' % levels ,'step']

Invoking with:

::

         fin+ 3

would expand to: ``['finish 3', 'step']``

If you were to add another parameter for ``step``, the note that the
invocation might be:

::

         fin+ 3 2

rather than ``fin+(3,2)`` or ``fin+ 3, 2``.

See also ``alias``, and ``info macro``.

Python
------

*python* [*-d* ]

Run Python as a command subshell. The *sys.ps1* prompt will be set to
``trepan2 >>>``.

If *-d* is passed, you can access debugger state via local variable
*debugger*.

To issue a debugger command use function *dbgr()*. For example:

::

      dbgr('info program')

Unalias
-------

**unalias** *alias-name*

Remove alias *alias-name*.

See also ``alias``.
