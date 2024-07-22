#!/usr/bin/env python
"General integration tests"
import unittest

import helper as Mhelper


class GeneralTests(unittest.TestCase):

    def test_step(self):
        """Test stepping, set skip, set trace"""
        right_template = None
        result = Mhelper.run_debugger(
            testname="step",
            dbgr_opts="--basename --highlight=plain --nx",
            python_file="gcd.py",
            right_template=right_template,
        )

        self.assertEqual(True, result, "debugger 'step' command comparision")
        return
    pass

if __name__ == "__main__":
    unittest.main()
