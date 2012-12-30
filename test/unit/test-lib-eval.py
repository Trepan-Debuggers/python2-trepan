#!/usr/bin/env python
'Unit test for pydbgr.lib.eval'
import unittest
from import_relative import import_relative

import_relative('lib', '...pydbgr', 'pydbgr')
Meval = import_relative('lib.eval', '...pydbgr', 'pydbgr')

class TestExtractExpression(unittest.TestCase):

    def test_extract_expression(self):
        for fragment, expect in (
            ('if condition(x):',     'condition(x)'),
            ('while expression:',    'expression'),
            ('return return_value',  'return_value'),
            ('nothing_to_be.done',   'nothing_to_be.done'),
            ):
            self.assertEqual(expect , Meval.extract_expression(fragment))
            pass
        pass
    pass

if __name__ == '__main__':
    unittest.main()
