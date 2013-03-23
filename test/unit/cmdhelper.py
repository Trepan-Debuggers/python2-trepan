# -*- coding: utf-8 -*-
""" Mock classes used for testing which in turn really come from 
pydbgr.processor.command.mock """

from import_relative import import_relative

default   = import_relative('lib.default', '...pydbgr') # Default settings
mock      = import_relative('processor.command.mock', '...pydbgr')

dbg_setup = mock.dbg_setup
