Files
=====

Specifying and examining files.

List (show me the code!)
------------------------

The list command will show you your source code::

::

        (trepan2) list 2
          1     #!/usr/bin/python
          2     """Greatest Common Divisor
          3
          4     Some characterstics of this program used for testing check_args() does
          5     not have a 'return' statement.
          6
          7     check_args() raises an uncaught exception when given the wrong number
          8     of parameters.
          9
         10  -> """
        (trepan2) list # keep going
         11     import sys
         12
         13     def check_args():
         14         if len(sys.argv) != 3:
         15             # Rather than use sys.exit let's just raise an error
         16             raise Exception, "Need to give two numbers"
         17         for i in range(2):
         18             try:
         19                 sys.argv[i+1] = int(sys.argv[i+1])
         20             except ValueError:
        (trepan2) import os.path  # Assumes set autoeval on
        (trepan2) list os.path 1 11
          1     """Common operations on Posix pathnames.
          2
          3     Instead of importing this module directly, import os and refer to
          4     this module as os.path.  The "os.path" name is an alias for this
          5     module on Posix systems; on other systems (e.g. Mac, Windows),
          6     os.path provides the same operations in a manner specific to that
          7     platform, and is an alias to another module (e.g. macpath, ntpath).
          8
          9     Some of this can actually be useful on non-Posix systems too, e.g.
         10     for manipulation of the pathname component of URLs.
         11     """
        (trepan2) list os.path.join
         51
         52     # Join pathnames.
         53     # Ignore the previous parts if a part is absolute.
         54     # Insert a '/' unless the first part is empty or already ends in '/'.
         55
         56     def join(a, *p):
         57         """Join two or more pathname components, inserting '/' as needed"""
         58         path = a
         59         for b in p:
         60             if b.startswith('/'):
        (trepan2) remember_this_line=17
        (trepan2) list remember_this_line
         12
         13     def check_args():
         14         if len(sys.argv) != 3:
         15             # Rather than use sys.exit let's just raise an error
         16             raise Exception, "Need to give two numbers"
         17         for i in range(2):
         18             try:
         19                 sys.argv[i+1] = int(sys.argv[i+1])
         20             except ValueError:
         21                 print "** Expecting an integer, got: %s" % repr(sys.argv[i])
         (trepan2)

There are many more options and possibilities so check out ``help list``
for details. If you are not using *trepan2* via some sort of front-end
program (e.g. I generally use `my GNU Emacs
front-end <http://github.com/rocky/emacs-dbgr>`__. Also see
[#Set\_Auto\_List] below.
