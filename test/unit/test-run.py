#!/usr/bin/env python
'Unit test for pydbgr.processor.command.run'
import inspect, os, sys, unittest

from import_relative import *

# FIXME: until import_relative is fixed
import_relative('pydbgr', '...', 'pydbgr')

Mexcept  = import_relative('exception', '...pydbgr', 'pydbgr')
Mrun     = import_relative('pydbgr.processor.command.run', '...', 'pydbgr')

from cmdhelper import dbg_setup

class TestRun(unittest.TestCase):
    """Tests RunCommand class"""

    def test_run(self):
        """Test processor.command.run.RunCommand.run()"""
        d, cp = dbg_setup()
        command = Mrun.RunCommand(cp)
        self.assertRaises(Mexcept.DebuggerRestart, command.run, ['run'])
        return

if __name__ == '__main__':
    unittest.main()
