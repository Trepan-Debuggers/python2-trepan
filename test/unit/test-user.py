#!/usr/bin/env python
'Unit test for pydbg.interface.user'
import inspect, os, sys, unittest

from import_relative import *
Muser = import_relative('interface.user', '...pydbg')

from cmdhelper import dbg_setup

class TestInterfaceUser(unittest.TestCase):
    """Tests StepCommand class"""

    def readline(self, answer):
        return answer

    def test_confirm(self):
        """Test interface.user.UserInterface.confirm()"""
        d, cp = dbg_setup()
        u = Muser.UserInterface()
        for s in ['y', 'Y', 'Yes', '  YES  ']: 
            u.input.readline = lambda: self.readline(s)
            self.assertTrue(u.confirm('Testing'))
            pass
        for s in ['n', 'N', 'No', '  NO  ']: 
            u.input.readline = lambda: self.readline(s)
            self.assertFalse(u.confirm('Testing'))
            pass
        # FIXME: Add checking default values. Checking looping 
        # values
        return
    # FIXME: more thorough testing of other routines in user.

if __name__ == '__main__':
    unittest.main()
