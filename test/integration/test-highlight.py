#!/usr/bin/env python
"General integration tests"
import sys, unittest
import os.path as osp

import helper as Mhelper


class GeneralTests(unittest.TestCase):

    def test_macro(self):
        """Test set/show highlight"""

        srcdir = osp.abspath(osp.dirname(__file__))
        datadir   = osp.join(srcdir, '..', 'data')

        if sys.version_info[0:2] <= (2, 4):
            rightfile = osp.join(datadir, "highlight-2.4.right")
        else:
            rightfile = osp.join(datadir, "highlight.right")

        result = Mhelper.run_debugger(testname='highlight',
                                      dbgr_opts='--basename ' +
                                      '--highlight=plain --nx',
                                      python_file='gcd.py',
                                      rightfile=rightfile)
        self.assertEqual(True, result, "'highlight' command comparision")
        return
    pass

if __name__ == "__main__":
    unittest.main()
