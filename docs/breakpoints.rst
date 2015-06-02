Breakpoints
===========

Making the program stop at certain points

.. toctree::
   :maxdepth: 1


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

Delete
------
**delete** [*bpnumber* [*bpnumber*...]]

Delete some breakpoints.

Arguments are breakpoint numbers with spaces in between.  To delete
all breakpoints, give no argument.  those breakpoints.  Without
argument, clear all breaks (but first ask confirmation).

See also the `clear` command which clears breakpoints by line/file
number.

Disable
-------
**disable** *bpnumber* [*bpnumber* ...]

Disables the breakpoints given as a space separated list of breakpoint
numbers. See also `info break` to get a list.

Enable
-------
**enable** *bpnumber* [*bpnumber* ...]

Enables the breakpoints given as a space separated list of breakpoint
numbers. See also `info break` to get a list.

Tbreak
-------
**tbreak** [*location*] [**if** *condition*]

With a line number argument, set a break there in the current file.
With a function name, set a break at first executable line of that
function.  Without argument, set a breakpoint at current location.  If
a second argument is `if`, subequent arguments given an expression
which must evaluate to true before the breakpoint is honored.

The location line number may be prefixed with a filename or module
name and a colon. Files is searched for using *sys.path*, and the `.py`
suffix may be omitted in the file name.

Examples:
+++++++++

   tbreak     # Break where we are current stopped at
   tbreak 10  # Break on line 10 of the file we are currently stopped at
   tbreak os.path.join # Break in function os.path.join
   tbreak os.path:45   # Break on line 45 of os.path
   tbreak myfile.py:45 # Break on line 45 of myfile.py
   tbreak myfile:45    # Same as above.

See also:
+++++++++
`break`.
