#!/usr/bin/env python
'Unit test for pydbgr.processor.command.testsub.trace'
import inspect, os, sys, unittest

from import_relative import *

top_builddir = os.path.join(os.path.pardir, os.path.pardir, 'pydbgr')
Mtrace = import_relative('processor.command.setsub.trace', 
                         top_builddir).command.setsub.trace

from cmdhelper import dbg_setup

class TestQuit(unittest.TestCase):
    """Tests TraceCommand class"""

    def test_quit(self):
        """Test processor.command.quit.QuitCommand.run()"""
        d, cp = dbg_setup()
        command = Mquit.QuitCommand(cp)
        Mset = import_relative('set', '..')
        d, cp = mock.dbg_setup()
        s = Mset.SetCommand(cp)
        sub = SetTrace(s)
        sub.name = 'trace'
        for args in (['on'], ['off'], ['line'], ['bogus'],
                     ['on', 'call', 'return']):
            sub.run(args)
            print d.settings['printset']
            print d.settings['trace']
            pass
        try:
            command.run(['quit'])
        except:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        return

if __name__ == '__main__':
    unittest.main()
