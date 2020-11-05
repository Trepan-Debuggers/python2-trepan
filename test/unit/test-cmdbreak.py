#!/usr/bin/env python2
'Unit test for trepan.processor.cmdproc'
import re, sys, unittest
import os.path as osp
from trepan.processor import cmdproc as Mcmdproc
from trepan.processor.command import mock as Mmock
from trepan.processor.cmdbreak import parse_break_cmd

def canonic_tuple(t):
    """
    Convert a tuple to a tuple ).

    Args:
        t: (todo): write your description
    """
    fname = t[1]
    if fname:
        if fname.endswith('.pyc'):
            fname = fname[:-1]
        got = list(t)
        got[1] = osp.basename(fname)
        t = tuple(got)
    return t


class TestCmdParse(unittest.TestCase):

    def setUp(self):
        """
        Sets the socket.

        Args:
            self: (todo): write your description
        """
        self.errors             = []
        self.msgs               = []
        self.d                  = Mmock.MockDebugger()
        self.cp                 = Mcmdproc.CommandProcessor(self.d.core)
        self.cp.intf[-1].msg    = self.msg
        self.cp.intf[-1].errmsg = self.errmsg
        return

    def errmsg(self, msg):
        """
        Add an error message

        Args:
            self: (todo): write your description
            msg: (str): write your description
        """
        self.errors.append(msg)
        return

    def msg(self, msg):
        """
        Add a message to a message.

        Args:
            self: (todo): write your description
            msg: (str): write your description
        """
        self.msg.append(msg)
        return

    def test_basic(self):
        """
        Test if the test.

        Args:
            self: (todo): write your description
        """

        self.cp.frame = sys._getframe()
        self.cp.setup()
        myfile = osp.basename(__file__)
        myfile = re.sub(r"pyc$", "py", myfile)

        for expect, cmd in (
                ( (None, None, None, None),
                  "break '''c:\\tmp\\foo.bat''':1" ),
                ( (None, None, None, None),
                  'break """/Users/My Documents/foo.py""":2' ),
                ( (None, myfile, 10, None),
                  "break 10" ),
                ( (None, None, None, None),
                   "break cmdproc.py:5" ) ,
                ( (None, None, None, None),
                   "break set_break()" ),
                ( (None, myfile, 4, 'i==5'),
                   "break 4 if i==5" ),
                ( (None, None, None, None),
                  "break cmdproc.setup()" ),
                ):
            args = cmd.split(' ')
            self.cp.current_command = cmd
            got = canonic_tuple(parse_break_cmd(self.cp, args))
            self.assertEqual(expect, tuple(got))
            # print(got)


        self.cp.frame = sys._getframe()
        self.cp.setup()

        # WARNING: magic number after f_lineno is fragile on the number of tests!
        # FIXME: can reduce by using .format() before test?
        break_lineno = self.cp.frame.f_lineno + 9
        for expect, cmd in (
                ( (None, myfile, break_lineno, None),
                    "break" ),
                ( (None, myfile, break_lineno, 'True'),
                    "break if True" ),
                ):
            args = cmd.split(' ')
            self.cp.current_command = cmd
            got = canonic_tuple(parse_break_cmd(self.cp, args))
            self.assertEqual(expect, got)
            print(parse_break_cmd(self.cp, args))

        print(break_lineno)
        pass
        return


if __name__ == '__main__':
    unittest.main()
    pass
