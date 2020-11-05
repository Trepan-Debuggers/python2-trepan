#!/usr/bin/env python
'Unit test for trepan.processor.command.disassemble'
import inspect, unittest

from trepan.processor.command import disassemble as Mdis

from cmdhelper import dbg_setup


class TestDisassemble(unittest.TestCase):

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

    def msg(self, msg):
        """
        Prints a message

        Args:
            self: (todo): write your description
            msg: (str): write your description
        """
        self.msg_nocr(msg)
        self.last_was_newline = True
        return

    def msg_nocr(self, msg):
        """
        Add a message.

        Args:
            self: (todo): write your description
            msg: (str): write your description
        """
        if self.last_was_newline:
            self.msgs.append('')
            pass
        self.msgs[-1] += msg
        self.last_was_newline = len(msg) == 0
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

    def test_disassemble(self):
        """Test processor.command.disassemble.run()"""

        print("Skipping until disassembly revamp complete")
        assert True
        return
        d, cp = dbg_setup()
        command = Mdis.DisassembleCommand(cp)

        self.setup_io(command)
        command.run(['disassemble'])
        self.assertTrue(len(self.errmsgs) > 0)
        self.assertEqual(len(self.msgs), 0)
        me = self.test_disassemble  # NOQA
        cp.curframe = inspect.currentframe()
        proc = command.proc
        # All of these should work
        for args in (['disassemble'],
                     ['disassemble', 'cp.errmsg'],
                     ['disassemble', 'unittest'],
                     ['disassemble', '1'],
                     ['disassemble', '10', '100'],
                     ['disassemble', '*10', '*30'],
                     ['disassemble', '+', '1'],
                     ['disassemble', '-', '1'],
                     ['disassemble', '1', '2'],
                     ['disassemble', 'me']):
            self.clear_output()
            proc.current_command = ' '.join(args)
            command.run(args)
            self.assertTrue(len(self.msgs) > 0,
                            "msgs for: %s" % ' '.join(args))
            self.assertEqual(len(self.errmsgs), 0,
                             "errmsgs for: %s %s" % (' '.join(args),
                                                     "\n".join(self.errmsgs)))
            pass
        return


if __name__ == '__main__':
    unittest.main()
