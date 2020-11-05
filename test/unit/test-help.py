#!/usr/bin/env python
'Unit test for trepan.processor.command.help'
import unittest

from trepan.processor.command import help as Mhelp, mock as Mmock
from trepan.processor import cmdproc as Mcmdproc


class TestHelp(unittest.TestCase):
    """Tests HelpCommand class"""

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
        self.cmd                = Mhelp.HelpCommand(self.cp)
        self.cmd.msg            = self.msg
        self.cmd.errmsg         = self.errmsg
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
        Convert a message to a message.

        Args:
            self: (todo): write your description
            msg: (str): write your description
        """
        self.msgs.append(msg)
        return

    def test_help_command(self):
        """Test we can run 'help *cmd* for each command"""

        for name in self.cp.commands.keys():
            self.cmd.run(['help', name])
            pass
        self.assertTrue(len(self.msgs) > 0, 'Should get help output')
        self.assertEqual(0, len(self.errors), 'Should not get errors')
        return

    def test_help_categories(self):
        """Test we can run 'help *cmd* for each category"""

        for name in Mhelp.categories.keys():
            self.cmd.run(['help', name])
            pass
        self.assertTrue(len(self.msgs) > 0, 'Should get help output')
        self.assertEqual(0, len(self.errors), 'Should not get errors')

        for name in Mhelp.categories.keys():
            self.cmd.run(['help', name, '*'])
            pass
        self.assertTrue(len(self.msgs) > 0, 'Should get help output')
        self.assertEqual(0, len(self.errors), 'Should not get errors')

        return

    def test_short_help(self):
        """Test each command has some sort of short help"""
        for cmd in list(self.cp.commands.values()):
            self.assertEqual(str, type(cmd.short_help))
            pass
        return

    pass
if __name__ == '__main__':
    unittest.main()
