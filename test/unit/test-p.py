#!/usr/bin/env python
'Unit test for pydbgr.processor.command.p'
import inspect, os, sys, unittest

from import_relative import *

Mp = import_relative('processor.command.p', '...pydbgr')

from cmdhelper import dbg_setup
import signal

class TestP(unittest.TestCase):
    """Tests PCommand class"""

    def setUp(self):
        self.errors = []
        self.msgs = []
        return

    def errmsg(self, msg):
        self.errors.append(msg)
        return

    def msg(self, msg):
        self.msgs.append(msg)
        return

    def test_p(self):
        """Test processor.command.p.PCommand.run()"""
        import inspect
        cmdproc     = import_relative('processor.cmdproc', '...pydbgr', 'pydbgr')
        debugger    = import_relative('debugger', '...pydbgr', 'pydbgr')
        d           = debugger.Debugger()
        cp          = d.core.processor
        cp.curframe = inspect.currentframe()
        cmd         = Mp.PrintCommand(cp)
        cmd.msg     = self.msg
        cmd.errmsg  = self.errmsg
        me = 10
        cmd.run(['print', 'me'])
        self.assertEqual('10', self.msgs[-1])
        cmd.run(['print', '/x', 'me'])
        self.assertEqual("'0xa'", self.msgs[-1])
        cmd.run(['print', '/o', 'me'])
        self.assertEqual("'012'", self.msgs[-1])
        return

if __name__ == '__main__':
    unittest.main()
