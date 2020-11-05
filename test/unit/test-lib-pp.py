#!/usr/bin/env python
'Unit test for trepan.lib.pp'
import sys, unittest

from trepan.lib import pp as Mpp


class TestLibPrint(unittest.TestCase):

    def setUp(self):
        """
        Set the set of the currently set.

        Args:
            self: (todo): write your description
        """
        self.msgs = []
        return

    def msg_nocr(self, msg):
        """
        Add a msgs message

        Args:
            self: (todo): write your description
            msg: (str): write your description
        """
        self.msgs = [msg]
        return

    def msg(self, msg):
        """
        Conveniohttp.

        Args:
            self: (todo): write your description
            msg: (str): write your description
        """
        self.msgs = [msg]
        return

    def notest_lib_pprint_simple_array(self):
        """
        A simple simple simple simple message.

        Args:
            self: (todo): write your description
        """
        Mpp.pprint_simple_array(list(range(50)), 53, self.msg_nocr, self.msg)
        self.assertEqual(
            ['[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11,\n'
             ' 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,\n'
             ' 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,\n'
             ' 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,\n'
             ' 48, 49]\n\n'], self.msgs)
        return

    pass

if __name__ == '__main__':
    unittest.main()
