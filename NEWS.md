trepan 1.2.3 2021-01-24
=======================

* Add `set tempdir` and `show tempdir`. In remote debugging this is useful
* eval?: add "and" and "or" by stripping out the final and/or
* deal wit no style set
* use PyPI term-background package
* fix bug in decompiling

trepan 1.2.2 2020-10-11
=======================

* Extend patsub's effect to breakpoint Hook the command processor file
  pattern substutition to python filecache's file pattern substitution
* Tolerate inspect.formatargvalues() errors
* Go over "set" subcommand processing
* Set min/max args for set patsub
* set style command error message

trepan 1.2.1 2020-08-30
=======================

* Add `info locals --list`
* Correct Formatting of 1-arg bytes in asm
* Get "set patsub" to substitute file paths e.g. "^/code" inside docker -> "/Users/rocky/project"

About "set patsub". We need to do the substitution in the debugger, not in
`pyficache` where we just want the presentation of the filename to be
different. The actual location is the name `pyficache` sees and gets
lines from.

trepan 1.2.0 2020-08-23
=======================

disassembly via [`xdis`](https://pypi.org/project/xdis/) now supports "extended" assembly listing which is new. Use that by default.

Commands have been gone over to be DRYer and use a more modern style of imports.
Small bugs have been fixed in conjunction with going over the commands.

New/Changed commands:

* `set asmfmt` will let you select between the different formats and
* `show asmfmt` will show you what format is in effect
* `info lines` shows more information about what lines can be breakpointed (have line number table offsets in code)
* `info offsets` shows you what offsets can be breakpointed (start on a line-number table entry)
* `info line` gives more information, i.e. offset info, for a given line.


trepan 1.1.0 2020-05-23 pyficache
=================================

* Incorporate a major update of pyficache which removes the coverage dependency.
* More Python source has been reformatted and imports revised along current thinking.
* Some errors in termination messages have been fixed.
* `--AST` renamed to `--tree` since that's what it is and `AST` it is not

trepan 1.0.0 2020-04-27 One oh
==============================

- Release to track changes in uncompyle6 and xdis
- deparsing fixes

trepan 0.8.7 2018-20-27 9 x 7 release
=====================================

- Command doc changes

trepan 0.8.7 2018-04-16  (no 0.8.5 or 0.8.6)

- gdb "backtrace" negative count documented and supported
- add `-d`, `--deparse` and `--source` options on `backtrace` command
- DRY uncompyle and deparsing code. Use newer API
- expand source-code line-number width to 4 places
- reinstante deparse

trepan 0.8.4 2018-02-5
======================


- Add `break!` to set a breakpoint whether trepan thinks
  there is a breakpoint
- Cache deparse info
- `set style` improvements
- Handle PyPy better
- `info locals *` and `info globals *` will list names
   in columnar form omitting values

trepan 0.8.3 2018-01-21
=======================

- Add `break!` and `b!` aliases to force setting a breakpoint on a line
- Update RsT
- print `p` and `pr` mean the same thing

trepan 0.8.2 2017-12-10

- Misc little fixes
- Go over RsT for revised `list` commands

trepan 0.8.1 2017-10-28
=======================

Fix botched release

- Packaging woes; was missing modules
- Correct documentation

trepan 0.8.0 2017-10-27
=======================

User incompatibilty alert!

We have redone location, breakpoint, and list-range parsing.

This release needs an explanation.

Code to parse commands like `list` and `breakpoint` were ugly and hard
to maintain. I hit a the tipping point in adding flexibility to the
"disassemble" command which allows address in addition to the usual
other kinds of locations.

Since version 0.6.3 when the `deparse` command was added, there has
been a hidden dependency of the the Earley parser.

That is now used to simplify parsing concepts like location,
list range, or breakpoint position.

In the process, I've gone over the syntax to make things more gdb
compatible. But of course gdb is also a moving target, so its syntax
has been extended and gotten more complicated as well.

In the olden days, I was sad that debuggers didn't follow someone
else's syntax but instead invented their own, sometimes incompatible
with gdb. Nowadays though it is a Herculean feat to come close to
matching gdb's syntax. Sigh.

The other problem with matching *gdb*'s syntax is that debugging Python
is enherently different from debugging a compiled language with object
files. Python's language model just isn't the same as C's.

So there are deviations. The biggest change that I suspect will impact
users is that function names in locations in this debugger needs a
trailing "()" to mark it as a function. This was not needed in
previous versions and it isn't needed in *gdb*.

Not implimented in our notion of location are things that feel
compiled-language object-file-ish. Specifying the function name inside
an object file, isn't the way Python (or most dynamic languages)
do things.  Instead you list the method/function inside a class or
module. And we allow this to be done off of variables and variables
holding instance methods.

Some things like ending at an address is not implemented as going
backwards in variable-length bytecode is a bit of work. Other things
of dubious merit I've omitted. The flexibility that is there
is probably overkill.

Speaking of reduced flexibility. Now with parser in place we no longer
support expressions as numbers in list commands. It's not in *gdb* and
I have a feeling  that too is overkill.


trepan 0.7.8 2017-07-10
=======================

- Release for updated `xdis` and botched RsT
- PyPy 2.x tolerance
- Small error message improvements

trepan 0.7.7 2017-07-10
=======================

- improve remote debugging:
  * scans for open ports
  * allow a socket to be passed in
  * start Celery remote debugging
- add `deval`, `deval?` commands: deparsed `eval` and `eval?`
- in python/shell don't go into post-mortem debugger on exception
- find source or decompile when bytecode is given
- Handle position in the presence of `eval()` and `exec()`
- show code via xdis when disassembling an entire function.
- improved terminal background detection respecting
  environment variables: `DARK_BG`, `COLORFGBG`
- deparse improvements:
  * do deparse offset fuzzing
  * show asm listing for opcode
  * add `-o` | `--offset` to indicate where to start deparsing from

trepan 0.7.6 2017-06-03
=======================

- Fix botched release and sync version numbers with trepan3k
- Corrected setup.py code, cheking and better error messaging
`- better stack trace position in the presense of eval() and exec()
- position in the presence of eval() and exec() via uncompyle6; this needs
  uncompyle6 0.11.0 or greater now
- better deparse command output shows grammar sysmbol on parent,
  and full disassembly line for instruction
- deparse offset fuzzing
- fix bugs in deparser option processing
- in disassembly of functions show function header
- go over docs `info.rst`, `pc.rst`

trepan 0.7.4 2017-06-03 Marilyn Frankel
=======================================

- Fix botched release
  * add RsT files
  * go over docs even more
  * fix packaging adminstrivia which botched release

trepan 0.7.3 2017-06-03
=======================

- Package name is now trepan2!
- Add version test in setup to avoid possible install from Python 3
- Resync version number with Python 3 trepan3k
- Add `info pc` command
- Show list of styles with `set style` (no style given)
- Add MS Windows kill with Python 2.6 tolerance
- Bugs in remote debugging tcpfns.py: handle "kill" better client.py: remove extra "\n"s
- Document `set substitute`
- Document `set style`
- `deparse` changes:
  * add `--offset`/`-O` option to show exact deparsable offsets
  * allow fuzzy offset deparsing via uncompyle6 deparse_around_offset
- `list` changes:
  * deparse when no source is available (e.g. on an exec or eval string)
- "set highlight" changes:
  * clear source-code cache after setting highlight
- "show display changes"
  * show display expression after setting it
- Update `MANIFEST.in` which should provide more reliable packaging
- `disassemble` changes:
  * better output using routines from `xdi`s package
- force deparse improvements by bumping uncompyle6 minimum version

trepan 0.6.5 2016-07-26
=======================

- PyPy tolerance
- Add `deparse` options `--parent` `--AST`, and `--offset`
- Use deparse bytecode to get source if we can't find it
- Some `flake8` linting

trepan 0.6.4 2015-12-31 - End of Year
=====================================

- follow _gdb_ `up`/`down` conventions
- Bump min package version requirements

trepan 0.6.3 2015-12-27 - Late Christmas
========================================

- deparses now via uncompyle6 package
- add `info code` command to show Python code properties
- add "assert" to "eval?" command
- add `trepan.api.debug(start_opts={'startup-profile': True})` to get your
  startup profile sourced
- Allow a frame object instead of a frame number in `frame` command

trepan 0.6.2 2015-12-11
=======================

- Add `deparse` command. Requires uncompyle2 to be activated

trepan 0.6.1 2015-12-10 - Dr Gecko
==================================

- add *gdb*-like `clear` command
- fallback to getlines for getting non-filename positions, e.g. inside compressed egg
- Remove spurious remap positions in showing location
- document installation and access from pytest
- bug fixes

trepan 0.6.0 2015-11-30
=======================

- Profile startup moved from `.trepanrc2` to ./config/trepany/profile
- Add ability to pygments style via `set style`. Add `show style`
- Add ability to remap a source file to another file name: `set substitute`
- Add *gdb*'s `set confirm`
- Fix highlight bugs and improve colors for dark backgrounds, e.g. emacs atom dark.
- Miscellaneous bug and doc fixes

trepan 0.5.3 2015-10-12
=======================

- Revise quit to handle threads

trepan 0.5.1 2015-08-16
=======================

- pytest support improvement: Add debug(level=...)
  The causes the debugger to skip recent frames used in setup.

trepan 0.5.0 2015-08-02
=======================

- Don't show an error if we can't import bpy or ipython - they are optional
- doc fixes

trepan 0.4.9 2015-06-12 Fleetwood
=================================

- add bpython shell.
- set default completion (not debugger completion) in python shell
- Save/restore ipython completion if we can do so
- don't highlight prompt when highlight is plain/off
- Add syntax help and go over docs, add links to readthedocs

trepan 0.4.8 2015-05-16
=======================

- Include instruction number in location
- Add "info *" and "info arg1, arg2".
- Add "info frame *number*
- Set/check max args in subcommands
- Add completion on "tbreak", "break" and "set highlight"
- Don't highlight prompt when highlight is plain or off
- eval? picks out EXPR in for VAR in EXPR:
- Update online-help

trepan 0.4.7 2015-05-16
=======================

- Better command completion for on display numbers and identifiers
  (commands: `enable`, `disable`, `info break`, `delete`, `debug`, `whatis`, `pydocx`,
   `pr`, `pp`)
- `info break [nums..]` allows giving breakpoint numbers to narrow results
- add `info frame` to show current call-stack information,
- add `info signals *` to show a list of signals
- fix misc bugs

trepan 0.4.6 2015-05-15
=======================

- Support for getting called from within ipython (--from_ipython)
  See also https://github.com/rocky/ipython-trepan/
- prompt is underlined if highlight is on
- Fix bug in string eval to file remapping
- Add boolean closed on I/O routines


trepan 0.4.5 2015-04-23
=======================

- Fix bug in `next` command
- Try to fix RsT in pypi

trepan 0.4.3 2015-02-17
=======================

- If help regexp matches a single command, give help for that.
- Doc fixes
- Sync with python3 code

trepan 0.4.2 2015-02-17
=======================

- Should work with pip without needing `--egg`. Thanks to Georg Brandl
- Go over `set`/`show` help
- Go over docs and increase docstring RsT use
- Finish removing flake8 warnings
- Fix bugs in startup-file loading
- Fix bug in signal-name lookup. From Georg Brandl

trepan 0.4.1 2014-12-23 Late SF
===============================

- Get computed_displaywidth from updated columnize. Should work on OSX
- Sections get an underline when we syntax highlight is not in effect
- Add README.rst for pypi
- flake8 lint warning/error reduction


trepan 0.4.0 2014-12-24 Ph. Mad.
================================

- Add `fin` and `kill!` aliases
- Fix bug in `eval?` for `elif`

trepan 0.3.9 2014-10-25
=======================

- Add/fix --client option. code.google.com issue #17.
- More lint warnings removed.

trepan 0.3.8 2014-10-25
=======================

- Put back namespace packages. pip works as long as `--egg` option is used
 easy_install just works. More flake8 linting.

trepan 0.3.7 2014-10-25
=======================

- More flake8 linting. Another attempt to get this to install cleanly
  with pip and easy_install. This time, for sure!
  For pip: nuke   namespace packages

trepan 0.3.6 2014-10-25
=======================

- More flake8 linting. Another attempt to get this to install cleanly with
  pip and easy_install.

trepan 0.3.5 2014-10-21
=======================

- More flake8 linting. Another attempt to get this to install cleanly with
  pip and easy_install.

trepan 0.3.4 2014-10-19
=======================

- Reduce import_relative, quit and restart should work better
- More linting.

trepan 0.3.3 2014-10-10
=======================

-  Another attempt to make this pip install cleanly

trepan 0.3.2 2014-10-10
=======================

-  Another attempt to make this pip install cleanly

trepan 0.3.1 2014-10-08
=======================

-  botched release 0.3.0

trepan 0.3.0 2014-10-08
=======================

-  make `quit` really quit rather than go into post-mortem.
-  reduce warnings

trepan 0.2.9 2014-10-04
=======================

- fixes to reduce namespace clashes until this can be rewritten better
- remote execution options `--host` and `--port`
- small bug fixes

trepan 0.2.8 2013-05-12
=======================

- redo botched release

trepan 0.2.7 2013-05-12
=======================

- Fill out command completion more
- Fix bug in removing a display.

trepan 0.2.6 2013-04-19
=======================

- Rename egg from `pydbgr` to `trepan`. Script to run is `trepan2`.
- Start command completion
- Command history reading and saving works.

0.2.6 2013-03-24
================

- Handle Python 2.4

0.2.5 2013-03-23
================

- eval? handles if/while expressions better
- Numerous small bug fixes
- Make code more Python3 compatible to reduce the difference between this
  and python3-trepan.
- Start linting code via pyflakes

0.2.4 2013-03-15 Ron Frankel Ides of March
===========================================

- Add debugger "alias" and "unalias" commands

- Better handling of "info args"

- Start Python3 compability. However for something that
  works with Python3 see work-in-progress
  https://code.google.com/p/python3-trepan/

0.2.3 2013-02-02
================

- Add debugger "macro" command
- Start Bullwinkle processor

0.2.2 01-12-13
==============

- More pervive use of ReStructuredText and fixes to the
  formatting code.

0.2.1 01-05-13
==============

- Add call stack and disassembly colorization
- Command docstring are now in ReStructuredText so they are
  colorized and reformatted according to width setting
- api run_eval() and and run_exec() strings are now saveed
  and remapped to a temporary file for front ends.
- debugger command names are downcased.
- Some code restructuring.


0.2.0 01-01-13
==============

- Port more of the trepanning debugger features here
  * Terminal output for errors, sections, and code syntax highlighting
  * Smart Eval (eval sections of the source line of code)

0.1.6 12-27-12
==============

- Try to repackage for 2.7 so we don't get easy install egg errors.
  (or at least fewer of them).

0.1.5 10-27-10
==============

- "p" command renamed to "pr" like trepanning debuggers
- set maxstrsize -> set maxstring and fix bug to update that
- remove pyflakes warnings
- show return value in nested debugging and add level of parenthsis in prompts
- report PC offset in info program and disassemble
- some bug fixes

0.1.4 06-12-10 the Fleetwood
============================

- Show return value when at a return event
- Fix up ipython %pydbgr support.
- Some support for nested debugging (debugger command "debug")
- eval'ing quit() is accepted as quit
- Debugger command "retval" becomes "info return" to match rbdbgr
- Some small bug fixes.


0.1.3 12-25-09
==============

- Small bugs in invoking without a Python program and off-by one in 'finish'
  command
- Remove emacs code. For emacs support see http://github.com/rocky/emacs-dbgr

0.1.2 10-27-09 Halala ngosuku lokuzalwa
=======================================

- When we are stopped at a breakpoint, make that the event.
- `info file xx lines` -> `info file xx brkpts`
- `info tracesets` -> `info events`
- `exit` doesn't need to have a stack to run
- allow entering the debugger without having to run a Python script
  (requested by Yaroslav Halchenko)
- `pydbgr.api.debug(step=ddd)` -> `pydbgr.api.debug(step_ignore=ddd)`
- allow getting regular expression patterns in help. (Suggested by Mike Welles)
- Misc doc and bug fixes
- add `edit` command

0.1.1 07-04-09
===============

- `sys.argv` had not been set correctly for debugged program. (Issue #1)
- Allow disassembly of compiled python files (`.pyc`)

0.1.0 03-15-09 - Ron Frankel Release
====================================

- Initial release
