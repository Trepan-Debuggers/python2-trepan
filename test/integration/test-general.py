#!/usr/bin/env python
"General integration tests"
import unittest

from helper import run_debugger


class GeneralTests(unittest.TestCase):

    def test_step(self):
        """Test stepping, set skip, set trace"""
        right_template = None
        result = run_debugger(
            testname="step",
            dbgr_opts="--basename --highlight=plain --nx",
            python_file="gcd.py",
            right_template=right_template,
            args=[3, 5],
        )

        self.assertEqual(True, result, "debugger 'step' command comparision")
        return
    pass

if __name__ == "__main__":
    unittest.main()
