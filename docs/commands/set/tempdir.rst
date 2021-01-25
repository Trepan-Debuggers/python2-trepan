.. index:: set; tempdir
.. _set_tempdir:

Set Tempdir
-----------

**set tempdir** *directory*

This is sometimes useful remote debugging where you might set up a
common shared location available between the debugged process and
the front end client.


Example:
++++++++

::

   set tempdir /code/tmp  # /code is a shared directory

.. seealso::

   :ref:`show tempdir <show_tempdir>`
