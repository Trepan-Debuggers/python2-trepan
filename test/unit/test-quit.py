#!/usr/bin/env python
'Unit test for pydbgr.processor.command.quit'
import inspect, os, sys, unittest

from import_relative import *

Mquit = import_relative('processor.command.quit', '...pydbgr')

from cmdhelper import dbg_setup

class TestQuit(unittest.TestCase):
    """Tests QuitCommand class"""

    def setUp(self):
        self.signal_caught = False
        return

    def test_quit(self):
        """Test processor.command.quit.QuitCommand.run()"""
        d, cp = dbg_setup()
        command = Mquit.QuitCommand(cp)
        try:
            command.run(['quit'])
        except:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        return

if __name__ == '__main__':
    unittest.main()
