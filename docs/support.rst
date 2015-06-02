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
