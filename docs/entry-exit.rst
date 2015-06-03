.. contents::

There are a couple ways you can enter the debugger:

-  Run the debugger initially
-  Add a call to the debugger inside your code
-  Run post-mortem debugging when an unexpected exception occurs
-  Set up an exception handler to enter the debugger on a signal

Invoking the Debugger Initially
===============================

The simplest way to debug your program is to call run ``trepan2``
specifying the name of your program and its options and any debugger
options:

.. code:: console

        $ cat test.py
        print 'Hello, World!'

        $ trepan2 test.py

For help on trepan2's options add the ``==help`` option.

.. code:: console

        $ trepan2 ==help
        Usage: trepan2 [debugger-options] [python-script [script-options...]]
        ...

To separate options to the program you want to debug from trepan2's
options put == after the debugger's options:

.. code:: console

      $ trepan2 ==trace == test.py ==test-option1 b c

If you have previously set up remote debugging using
``trepan2 ==server``, you'll want to run the client version of *trepan2*
which is a separate program ``trepan2c``.

Calling the debugger from IPython
=================================

Installing the IPython extension
*********************************

Use the `trepan IPython extension <https://pypi.python.org/pypi?:action=display&name=trepan>`_.

To install execute the the following code snippet in an IPython shell or IPython notebook cell:

.. code:: console

    %install_ext https://raw.github.com/rocky/ipython-trepan/master/trepanmagic.py
    %load_ext trepanmagic


or put *trepanmagic.py* in `$HOME/.python/profile_default/startup`:

.. code:: console

    cd `$HOME/.python/profile_default/startup`:
    wget https://raw.github.com/rocky/ipython-trepan/master/trepanmagic.py

Trepan IPython Magic Functions
*******************************

After installing the trepan extension, the following IPython magic functions are added:

* `%trepan_eval`  evaluate a Python statement under the debugger
* `%trepan` run the debugger on a Python program
* `%trepan_pm`  do post-mortem debugging

Example
*******

.. code:: console

       $ ipython
       Python 2.7.8 (default, Apr  6 2015, 16:25:30)
       ...

       In [1]: %load_ext trepanmagic
       trepanmagic.py loaded
       In [2]: import os.path
       In [3]: %trepan_eval(os.path.join('foo', 'bar'))
       (/tmp/eval_stringS9ST2e.py:1 remapped <string>): <module>
       -> 1 (os.path.join('foo', 'bar'))
       (trepan2) s
       (/home/rocky/.pyenv/versions/2.7.8/lib/python2.7/posixpath.py:68): join
       -> 68 def join(a, *p):
       (trepan2) s
       (/home/rocky/.pyenv/versions/2.7.8/lib/python2.7/posixpath.py:73): join
       == 73     path = a
       (trepan2) c
       Out[3]: 'foo/bar'
       In [4]:

See also the `examples <https://github.com/rocky/ipython-trepan/tree/master/examples>`_ directory.


Calling the debugger from an Interactive Python Shell
=====================================================

*Note: by "interactive python shell" I mean running "python" or "python -i" and this is distinct from going into IPython which was covered in the last section.*

Put these lines in a file::

.. code:: python

	  import inspect
	  from trepan.api import run_eval
	  def debug(str):
	    frame = inspect.currentframe()
	    return run_eval(str, globals_=frame.f_globals, locals_=frame.f_locals)
	  print("pythonrc loaded") # customize or remove this

A copy of the above can be found `here <https://github.com/rocky/python2-trepan/blob/master/PYTHONSTARTUP/pythonrc>`_. I usually put these line in `$HOME/.pythonrc`. Set the environment variable *PYTHONSTARTUP* to `$HOME/.pythonrc`.

After doing this, when you run `python -i` you should see on entry the *print* message from the file. For example;

.. code:: console

   	  $ python -i
	  Python ...
	  Type "help", "copyright", "credits" or "license" for more information.
	  pythonrc loaded
	  >>>

If you see the above "pythonrc" message, great! If not, it might be that *PYTHONSTARTUP* is not defined. Here run:

.. code:: console

	  >>> path="pythonrc" # customize to location of file
          >>> exec(open(path).read())
	  pythonrc loaded
	  >>>

and you should see the "pythonrc" message as shown above.

Once that code is loaded, the *debug()* function is defined. To debug some python code, you can call that function. Here is an example:

.. code:: console

    >>> import os.path
    >>> debug('os.path.join("a", "b")')
    (/tmp/eval_stringBMzXCQ.py:1 remapped <string>): <module>
    -> 1 os.path.join("a", "b")
    (trepan2) step
    (/home/rocky/.pyenv/versions/2.7.8/lib/python2.7/posixpath.py:68): join
    -> 68 def join(a, *p):
    (trepan2) continue
    'a/b'
    >>>

Note in the above, we pass to the *debug()* function a *string*.
That is, we pass `'os.path.join("a", "b")'`, not
`os.path.join("a", "b")` which would have the effect of running the code to be evaluated first *before* calling *debug()*. This is not an error, but debugging evaluating a string, is probably not what you want to do.

*To do: add and document run_call()*

Calling the debugger from your program
======================================

Sometimes it is not feasible to invoke the program from the debugger.
Although the debugger tries to set things up to make it look like your
program is called, sometimes the differences matter. Also the debugger
adds overhead and slows down your program.

Another possibility then is to add statements into your program to call
the debugger at the spot in the program you want. To do this,
``import trepan.api`` and make a call to *trepan.api.debug()*. For
example:

.. code:: python

        # Code run here trepan2 doesn't even see at all.
        # ...
        from trepan.api import debug
        # trepan is accessible but inactive.
        # work, work, work...
        debug() # Get me into the debugger!

Since *debug()* is a function, call it can be nested inside some sort of
conditional statement allowing one to be very precise about the
conditions you want to debug under. And until first call to *debug()*,
there is no debugger overhead.

*debug()* causes the statement after the call to be stopped at.
Sometimes though there is no after statement. In this case, adding the
named parameter ``step_ignore=0`` will cause the debugger to be entered
inside the *debug()* call:

.. code:: python

          # ...
          def foo():
             # some code
             debug(step_ignore=0) # Stop before even returning from the debug() call
          foo()  # Note there's no statement following foo()

Set up an exception handler to enter the debugger on a signal
=============================================================

This is really just a variation of one of the other methods. To install
and call the debugger on signal *USR1*:

.. code:: python

        import signal
        def signal_handler(num, f):
            from trepan.api import debug; debug()
           return
        signal.signal(signal.SIGUSR1, signal_handler)
        # Go about your business...

However, if you have entered the debugger either by running intially or
previously via a debug() call trepan2 has already set up such default
handlers for many of the popular signals, like *SIGINT*. To see what
*trepan2* has installed use the ``info signals`` command:

::

        (trepan2) info signals INT
         Signal        Stop   Print   Stack   Pass    Description
         SIGINT        Yes    Yes     No      No      Interrupt
        (trepan2) info signals
        Signal        Stop    Print   Stack   Pass    Description

        SIGHUP        Yes     Yes     No      No      Hangup
        SIGSYS        Yes     Yes     No      No      Bad system call
        ...

Commonly occuring signals like *CHILD* and unmaskable signals like
*KILL* are not intercepted.

Startup Profile
===============

A startup profile is a text file that contains debugger commands. For
example it might look like this:

.. code:: console

      $ cat ~/.trepan2rc
      set autolist
      set different on
      set autoeval on
      print("My trepan2 startup file loaded")
      $
