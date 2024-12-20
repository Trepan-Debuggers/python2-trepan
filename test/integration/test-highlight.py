#!/usr/bin/env python
"General integration tests"
import unittest

from helper import run_debugger
from xdis import PYTHON_VERSION_TRIPLE


class GeneralTests(unittest.TestCase):
    def test_macro(self):
        """Test set/show highlight"""
        if PYTHON_VERSION_TRIPLE >= (3, 8):
            right_template = "%s-38.right"
        else:
            right_template = None
        result = run_debugger(
            testname="highlight",
            dbgr_opts="--basename --highlight=plain --style=none --nx",
            python_file="gcd.py",
            right_template=right_template,
            args=[3, 5],
        )
        self.assertEqual(True, result, "'highlight' command comparision")
        return

    pass


if __name__ == "__main__":
    unittest.main()
