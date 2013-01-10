#!/usr/bin/env python
'Unit test for pydbgr.lib.file'
import unittest
import StringIO
from pygments.lexers import RstLexer
from import_relative import import_relative

import_relative('lib', '...pydbgr', 'pydbgr')
Mformat = import_relative('lib.format', '...pydbgr', 'pydbgr')

class TestLibFile(unittest.TestCase):

    def test_basic(self):

        # Could be in setup()
        rst_lex  = RstLexer()
        rst_filt = Mformat.RstFilter()
        rst_lex.add_filter(rst_filt)
        rst_tf = Mformat.MonoRSTTerminalFormatter()
        text = '`A` very *emphasis* **strong** `code`'
        got = Mformat.highlight(text, rst_lex, rst_tf)
        self.assertEqual('"A" very *emphasis* STRONG "code" ', got)
        return
    pass

if __name__ == '__main__':
    unittest.main()
