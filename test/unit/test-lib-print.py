#!/usr/bin/env python
'Unit test for pydbg.lib.print'
import inspect, os, sys, unittest
from import_relative import *

Mprint = import_relative('lib.print', '...pydbg')

class TestLibPrint(unittest.TestCase):

    def test_lib_printf(self):
        self.assertEqual('037', Mprint.printf(31, "/o"))
        self.assertEqual('00011111', Mprint.printf(31, "/t"))
        self.assertEqual('!', Mprint.printf(33, "/c"))
        self.assertEqual('0x21', Mprint.printf(33, "/x"))
        return
    
    pass

if __name__ == '__main__':
    unittest.main()
