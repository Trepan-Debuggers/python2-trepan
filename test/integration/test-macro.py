#!/usr/bin/env python
"General integration tests"
import sys, unittest
import os.path as osp

import helper as Mhelper


class GeneralTests(unittest.TestCase):

    def test_macro(self):
        """Test macro and info macro"""
        srcdir = osp.abspath(osp.dirname(__file__))
        datadir   = osp.join(srcdir, '..', 'data')

        vers_info = sys.version_info[0:2]
        if vers_info <= (2, 4):
            rightfile = osp.join(datadir, "macro-2.4.right")
        elif vers_info == (2, 5):
            rightfile = osp.join(datadir, "macro-2.5.right")
        else:
            rightfile = osp.join(datadir, "macro.right")

        result = Mhelper.run_debugger(testname='macro',
                                      dbgr_opts='--basename ' +
                                      '--highlight=plain --nx',
                                      python_file='gcd.py',
                                      rightfile=rightfile)
        self.assertEqual(True, result, "debugger 'macro' command comparision")
        return
    pass

if __name__ == "__main__":
    unittest.main()
