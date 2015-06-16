.. _kill:

Kill
----

**kill** [ *signal-number* ]

Send this process a POSIX signal ('9' for 'kill -9')

9 is a non-maskable interrupt that terminates the program. If program
is threaded or worse, threaded and deadlocked, you may need to use
this command to terminate the program.

However other signals, such as those that allow for the debugged to
handle them can be sent.

.. seealso::

   :ref:`quit <quit>` for less a forceful termination command.
   :ref:`run <run>` and :ref:`restart <restart>` are ways to restart the debugged program.
