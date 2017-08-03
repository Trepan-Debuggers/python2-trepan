#!/usr/bin/env python
"General integration tests"
import sys, unittest
import os.path as osp

import helper as Mhelper


class GeneralTests(unittest.TestCase):

    def test_step(self):
        """Test stepping, set skip, set trace"""
        srcdir = osp.abspath(osp.dirname(__file__))
        datadir   = osp.join(srcdir, '..', 'data')
        if sys.version_info[0:2] <= (2, 4):
            rightfile = osp.join(datadir, "step-2.4.right")
        else:
            rightfile = osp.join(datadir, "step.right")

        result = Mhelper.run_debugger(testname='step',
                                      dbgr_opts='--basename --highlight=plain',
                                      python_file='gcd.py',
                                        rightfile=rightfile)
        self.assertEqual(True, result, "debugger 'step' command comparision")
        return
    pass

if __name__ == "__main__":
    unittest.main()
