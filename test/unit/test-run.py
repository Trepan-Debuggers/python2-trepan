#!/usr/bin/env python
'Unit test for pydbg.processor.command.run'
import inspect, os, sys, unittest

from import_relative import *

# FIXME: until import_relative is fixed
import_relative('pydbg', '...', 'pydbg')

Mdebugger  = import_relative('debugger', '...pydbg', 'pydbg')
Mrun       = import_relative('pydbg.processor.command.run', '...', 'pydbg')

from cmdhelper import dbg_setup

class TestRun(unittest.TestCase):
    """Tests RunCommand class"""

    def test_run(self):
        """Test processor.command.run.RunCommand.run()"""
        d, cp = dbg_setup()
        command = Mrun.RunCommand(cp)
        self.assertRaises(Mdebugger.DebuggerRestart, command.run, ['run'])
        return

if __name__ == '__main__':
    unittest.main()
