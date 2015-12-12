.. _deparse:

Deparse (CPython bytecode deparser)
---------------------------------

**deparse** [offset] [-p]
       **deparse** .

deparse around where the program is currently stopped. If no offset is given
we use the current frame offset. If `-p` is given, include parent information.

In the second form, deparse the entire function or main program you are in.
Output is colorized the same as source listing. Use `set highlight plain` to turn
that off.

Examples:
+++++++++

::

       deparse  # deparse current location
       deparse -p # deparse current location enclosing context
       deparse .  # deparse current function or main

See also:
+++++++++

:ref:`disassemble <disassemble>`, :ref:`list <list>`, and :ref:`set_highlight <set_highlight>`
