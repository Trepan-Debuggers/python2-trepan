#!/usr/bin/env python
'Unit test for pydbgr.exception'
import unittest
from import_relative import import_relative

Mexcept = import_relative('exception', '...pydbgr')

class TestDeguggerExcept(unittest.TestCase):

    def test_debugger_restart(self):
        try:
            raise Mexcept.DebuggerRestart(['a', 'b'])
        except Mexcept.DebuggerRestart:
            import sys
            self.assertEqual(['a', 'b'], sys.exc_value.sys_argv)
        else:
            self.assertFalse(True)
        pass
        return
        
if __name__ == '__main__':
    unittest.main()
