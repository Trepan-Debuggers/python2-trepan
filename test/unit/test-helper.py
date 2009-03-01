#!/usr/bin/env python
# -*- coding: utf-8 -*-
'Unit test for the debugger pydbgr.frame'
import inspect, os, sys, unittest
from import_relative import *

Mclifns = import_relative('clifns', '...pydbgr')

class TestAPIHelper(unittest.TestCase):
    
    def test_is_ok_line_for_breakpoint(self):
        filename =  __file__
        if len(filename) > 4 and filename[-4:] == '.pyc':
            filename = filename[:-1]
        self.assertFalse(Mclifns.is_ok_line_for_breakpoint(filename, 
                                                           2, sys.stdout.write))
        self.assertTrue(Mclifns.is_ok_line_for_breakpoint(filename, 
                                                          4, sys.stdout.write))
        
        return

if __name__ == '__main__':
    unittest.main()
