This is a rewrite of the Python debugger, pydb.py, itself a derivative
of the stock Python debugger pdb.

Some of the core routines include handling code stepping, implementing
breakpoints (setting/removing them and checking whether one has
occurred), and registering/unregistering a code to be debugged.  The
intention is that IDE frameworks like Eclipse, Aptana or Netbeans and
alternative Python implementation should be able to use pieces of the
debugger as they see fit.

The command API portion of the debugger is largely modeled on the
GNU GDB model. A command-line interface (CLI) is provided.

There's a lot of cool stuff here that's not in pydb. 

* out-of-process debugging. You can now debug your program in a different
  process or even a different computer on a different network

* Better stepping granularity. Sometimes you want small steps, and
  sometimes large stepping. This fundamental issue is handled in
  a couple ways:

    - step+, step-, next+, next- commands. Force stepping/nexting to a
      different line. "set different" does this globally
   
    - one can set a filter set. If you just want to stop at line
      events (which is largely what you happens in pdb) you can. If
      however you just want to stop at calls and returns, and
      exceptions you can. Or pick some combination.
      
* In conjunction with handling *all* events by default,
  the event status is shown when stopped. The reason for stopping
  is also available via "info program". 

* event tracing of calls and returns. I'm not sure why this was not
  done before. Probably because of the lack of the ability to set and
  move by different granularities, tracing calls and returns lead to
  too many unintersting stops (such as at the same place you just were
  at). Also, stopping on function definitions probably also added to
  this tedium.

* We do more in the way of looking at the bytecodes to give better
  information. Through this we can provide:

  - a "skip" command. It is like the "jump" command, but you don't have to
    deal with line numbers.

  - disassembly of code fragments. You can now disassemble relative to the
    stack frames you are currently stopped at.

  - Better interpretation of where you are when inside execfile or exec.
    (But really though this is probably a Python compiler misfeature.)

  - Check that breakpoints are set only where they make sense. (Future
    planned)

  - A more accurate determination of if you are at a function-defining
    "def" statement (because the caller instruction contains
    "MAKE_FUNCTION".)

* egg installable.

* Debugger plays nice with other trace hooks. You can have several
  debugger objects.

* These don't directly effect end-users, but if you are developing the
  code they do. And keeping developers happy is a good thing. TM

  - more modulular. 

    o Commands and subcommands are individual classes now, not methods
      in a class. This means they now have properties like the context
      in which they can be run, minimum abbreviation name or alias
      names. To add a new command you basically add a file in a
      directory.
   
    o I/O is it's own layer. This simplifies interactive readline
      behavior from reading commands over a TCP socket.

    o An interface is it's own layer. Local debugging, remote
      debugging, running debugger commands from a file ("source") are
      different interfaces. This means, for example, that we are able
      to give better error reporting if a debugger command file has an
      error.

  - more testable. Much more unit and functional tests. pydb's integration
    test will eventually be added too. (As soon as we have something to 
    integrate against.)

Of course, I think pydb has a number of cool things that are not in
the stock Python debugger, pdb. 

