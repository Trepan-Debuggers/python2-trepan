# Copyright (C) 2010 Rocky Bernstein <rocky@gnu.org>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

## Note: the version number (the 2nd parameter in AC_INIT) 
## is picked up inside the Python debugger script.

m4_include([version.m4])
AC_INIT([pydbgr],VERSION_NUMBER,[pydbgr@googlegroups.com])
AC_DEFINE([PACKAGE], [pydbgr], [Modular Python Debugger])

# The below file sets veraible VERSION
. ./pydbgr/VERSION.py

PYDBGR_VERSION=$VERSION
AC_SUBST(PYDBGR_VERSION)
PACKAGE_VERSION=$VERSION
AM_MAINTAINER_MODE
AC_ARG_PROGRAM
AM_INIT_AUTOMAKE

AC_CONFIG_FILES([Makefile version.m4])
AC_OUTPUT
