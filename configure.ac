AC_INIT(pydbgr-extra, 0.1.1,)
AC_CONFIG_SRCDIR(emacs/pydbgr.el)
AM_INIT_AUTOMAKE

##
## Find out where to install the debugger emacs lisp files
##
AM_PATH_LISPDIR
AM_CONDITIONAL(INSTALL_EMACS_LISP, test "x$lispdir" != "x")

AC_CONFIG_FILES([emacs/Makefile Makefile])
AC_OUTPUT
