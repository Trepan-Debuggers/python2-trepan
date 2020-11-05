#!/usr/bin/env python
import sys
from fn_helper import compare_output, strarray_setup

if (sys.version_info >= (2, 7, 0)):
    import unittest   # NOQA
else:
    import unittest2 as unittest  # NOQA

class TestNext(unittest.TestCase):
    print("test ", __file__, "skipped")

    @unittest.skip("FIXME: figure out why this doesn't work")
    def test_next_same_level(self):
        """
        Determine the next level.

        Args:
            self: (todo): write your description
        """

        # See that we can next with parameter which is the same as 'next 1'
        cmds = ['next', 'continue']
        d = strarray_setup(cmds)
        d.core.start()
        x = 5
        y = 6
        d.core.stop()
        out = ['-- x = 5',
               '-- y = 6']
        compare_output(self, out, d, cmds)

        # # See that we can next with a computed count value
        # cmds = ['next 5-3', 'continue']
        # d = strarray_setup(cmds)
        # d.core.start()
        # x = 5  # NOQA
        # y = 6  # NOQA
        # z = 7  # NOQA
        # d.core.stop(options={'remove': True})
        # out = ['-- x = 5  # NOQA',
        #        '-- z = 7  # NOQA']
        # compare_output(self, out, d, cmds)
        return

    @unittest.skip("FIXME: figure out why this doesn't work")
    def test_next_between_fn(self):
        """
        Determine the next fact for the next fact file.

        Args:
            self: (todo): write your description
        """
        # Next over a function
        def fact(x):
            """
            Returns the fact of x.

            Args:
                x: (array): write your description
            """
            if x <= 1: return 1
            return fact(x-1)
        cmds = ['next', 'continue']
        d = strarray_setup(cmds)
        d.core.start()
        x = fact(4)  # NOQA
        y = 5  # NOQA
        d.core.stop(options={'remove': True})
        out = ['-- x = fact(4)  # NOQA',
               '-- y = 5  # NOQA']
        compare_output(self, out, d, cmds)
        return

    def test_next_in_exception(self):
        """
        Determine the next factgy.

        Args:
            self: (todo): write your description
        """
        return

        def boom(x):
            """
            Returns true if x is a boolean value.

            Args:
                x: (int): write your description
            """
            y = 0/x  # NOQA
            return

        def buggy_fact(x):
            """
            Buggygygy fact.

            Args:
                x: (todo): write your description
            """
            if x <= 1: return boom(0)
            return buggy_fact(x-1)
        cmds = ['next', 'continue']
        d = strarray_setup(cmds)
        try:
            d.core.start()
            x = buggy_fact(4)  # NOQA
            y = 5  # NOQA
            self.assertTrue(False, 'should have raised an exception')
        except ZeroDivisionError:
            self.assertTrue(True, 'Got the exception')
            pass
        d.core.stop(options={'remove': True})

        out = ['-- x = buggy_fact(4)  # NOQA',
               '!! x = buggy_fact(4)  # NOQA']
        compare_output(self, out, d, cmds)
        return

    pass

if __name__ == '__main__':
    unittest.main()
