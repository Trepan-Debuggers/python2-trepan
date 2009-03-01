# -*- coding: utf-8 -*-
""" Mock classes used for testing which in turn really come from 
pydbg.processor.command.mock """

import os
from import_relative import *

default   = import_relative('lib.default', '...pydbg') # Default settings
mock      = import_relative('processor.command.mock', '...pydbg')

dbg_setup = mock.dbg_setup
