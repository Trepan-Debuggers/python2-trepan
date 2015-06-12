.. _trepan2c:

trepan2c (Python2 client to connect to remote trepan session)
#############################################################

Synopsis
--------

**trepan2c** [ *debugger-options* ] [ \-- ] [ *python-script* [ *script-options* ...]]


Description
-----------

Run the Python2 trepan debugger client to connect to an existing out-of-process Python *trepan* session


Options
-------

:-h, \--help:
   Show the help message and exit

:-x, \--trace:
   Show lines before executing them.

:-H *IP-OR-HOST*, \--host= *IP-OR-HOST*:
   connect to *IP* or *HOST*

:-P *NUMBER, \--port= *NUMBER*:
   Use TCP port number NUMBER for out-of-process connections.

:\--pid=*NUMBER*:
   Use PID to get FIFO names for out-of-process connections.

See also
--------

:ref:`trepan3k` (1), :ref:`trepan2c` (1), :ref:`trepan3kc`

Full Documentation is available at http://python2-trepan.readthedocs.org
