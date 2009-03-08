#!/usr/bin/env python
'Unit test for pydbgr.processor.command.disassemble'
import inspect, os, sys, unittest
from import_relative import import_relative

import_relative('pydbgr', '...', 'pydbgr')
Mdis = import_relative('processor.command.disassemble', '...pydbgr')

from cmdhelper import dbg_setup

class TestDisassemble(unittest.TestCase):

    def msg(self, msg):
        self.msgs.append(msg)
    def msg_nocr(self, msg):
        pass
    def errmsg(self, msg):
        self.errmsgs.append(msg)
        pass
        
    def test_quit(self):
        """Test processor.command.disassemble.run()"""
        d, cp = dbg_setup()
        command = Mdis.DisassembleCommand(cp)
        command.msg = self.msg
        command.errmsg = self.errmsg
        command.msg_nocr = self.msg_nocr
        self.msgs = []
        self.errmsgs = []
        command.run(['disassemble'])
        self.assertTrue(len(self.errmsgs) > 0)
        self.assertEqual(len(self.msgs), 0)
        me = self.test_quit
        cp.curframe = inspect.currentframe()
        # All of these should work
        for args in (['disassemble'],
                     ['disassemble', '1'],
                     ['disassemble', '10', '100'],
                     ['disassemble', '+', '1'],
                     ['disassemble', '-', '1'],
                     ['disassemble', '+1', '2'],
                     ['disassemble', '-1', '2'],
                     ['disassemble', 'me']):
            self.msgs = []
            self.errmsgs = []
            command.run(args)
            self.assertTrue(len(self.msgs) > 0)
            self.assertEqual(len(self.errmsgs), 0)
            pass
        return


if __name__ == '__main__':
    unittest.main()
