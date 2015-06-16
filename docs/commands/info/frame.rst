.. _info_frame:

**info frame** [ *frame-number* ]


Info Frame
----------

Show the detailed information *frame-number* or the current frame if
*frame-number* is not specified.

Specific information includes:

* the frame number
* the source-code line number that this frame is stopped in
* the last instruction executed; -1 if the program are before the first instruction
* a function that tracing this frame or `None`
* Whether the frame is in restricted execution

.. seealso::

   :ref:`info locals <info_locals>`, :ref:`info globals <info_globals>`,
   :ref:`info args <info_args>`
