#!/usr/bin/env python
'Unit test for trepan.exception'
import unittest

from trepan import exception as Mexcept


class TestDeguggerExcept(unittest.TestCase):

    def test_debugger_restart(self):
        """
        Test if the debug.

        Args:
            self: (todo): write your description
        """
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
