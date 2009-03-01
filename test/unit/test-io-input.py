#!/usr/bin/env python
# -*- coding: utf-8 -*-
'Unit test for pydbg.io.input'
import operator, os, sys, unittest
from import_relative import *

Minput = import_relative('io.input', '...pydbg')
from pydbg.io.input  import DebuggerUserInput

class TestDebuggerInput(unittest.TestCase):
    
    def test_DebuggerInput(self):
        inp = DebuggerUserInput('test-io-input.py')
        self.assertTrue(inp, 'Should have gotten a DebuggerInput object back')
        line = inp.readline()
        self.assertEqual('#!/usr/bin/env python', line)
        inp.close()
        # Should be okay
        inp.close() 
        return

if __name__ == '__main__':
    unittest.main()
