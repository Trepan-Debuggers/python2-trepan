#!/usr/bin/env python
'Unit test for debugger info file'
import inspect, unittest

from trepan import debugger as Mdebugger
from trepan.processor.command import info as Minfo
from trepan.processor.command.info_subcmd import files as MinfoFile

from cmdhelper import dbg_setup


class TestInfoFile(unittest.TestCase):

    # FIXME: put in a more common place
    # Possibly fix up Mock to include this
    def setup_io(self, command):
        """
        Setup a command.

        Args:
            self: (todo): write your description
            command: (str): write your description
        """
        self.clear_output()
        command.msg = self.msg
        command.errmsg = self.errmsg
        command.msg_nocr = self.msg_nocr
        return

    def clear_output(self):
        """
        Clear the output.

        Args:
            self: (todo): write your description
        """
        self.msgs = []
        self.errmsgs = []
        self.last_was_newline = True
        return

    def msg_nocr(self, msg):
        """
        Nocr message.

        Args:
            self: (todo): write your description
            msg: (str): write your description
        """
        if len(self.msgs) > 0:
            self.msgs[-1] += msg
        else:
            self.msgs += msg
            pass
        return

    def msg(self, msg):
        """
        Convert a message to a message

        Args:
            self: (todo): write your description
            msg: (str): write your description
        """
        self.msgs += [msg]
        return

    def errmsg(self, msg):
        """
        Add an error message

        Args:
            self: (todo): write your description
            msg: (str): write your description
        """
        self.errmsgs.append(msg)
        pass

    def test_info_file(self):
        """
        Test the test info file info file.

        Args:
            self: (todo): write your description
        """
        d = Mdebugger.Debugger()
        d, cp = dbg_setup(d)
        command = Minfo.InfoCommand(cp, 'info')

        sub = MinfoFile.InfoFiles(command)
        self.setup_io(sub)
        sub.run([])
        self.assertEqual([], self.msgs)
        cp.curframe = inspect.currentframe()
        for width in (80, 200):
            # sub.settings['width'] = width
            sub.run(['test-info-file.py', 'lines'])
            sub.run([])
            pass
        pass

if __name__ == '__main__':
    unittest.main()
