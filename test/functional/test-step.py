#!/usr/bin/env python
import tracer
from fn_helper import strarray_setup, compare_output
import sys

if (sys.version_info >= (2, 7, 0)):
    import unittest   # NOQA
else:
    import unittest2 as unittest  # NOQA


class TestStep(unittest.TestCase):
    print("test ", __file__, "skipped")

    def test_step_same_level(self):
        """
        Determine the test level of the test.

        Args:
            self: (todo): write your description
        """
        return

        # See that we can step with parameter which is the same as 'step 1'
        cmds = ['step', 'continue']
        d = strarray_setup(cmds)
        d.core.start()
        ##############################
        x = 5  # NOQA
        y = 6  # NOQA
        ##############################
        d.core.stop()
        out = ['-- x = 5',
               '-- y = 6\n']
        compare_output(self, out, d, cmds)
        return

    @unittest.skip("Need to fix")
    def test_step_computed_valued(self):
        """
        Runs the yamputed test.

        Args:
            self: (todo): write your description
        """
        # See that we can step with a computed count value
        cmds = ['step 5-3', 'continue']
        d = strarray_setup(cmds)
        d.core.start()
        ##############################
        x = 5
        y = 6
        z = 7
        ##############################
        d.core.stop(options={'remove': True})
        out = ['-- x = 5',
               '-- z = 7']
        compare_output(self, out, d, cmds)

        # Test step>
        cmds = ['step>', 'continue']
        d = strarray_setup(cmds)
        d.core.start()
        ##############################
        x = 5

        def foo():
            """
            Decorator to add the function to use this.

            Args:
            """
            return
        y = 6  # NOQA
        foo()
        ##############################
        d.core.stop(options={'remove': True})
        out = ['-- x = 5',
               '-> def foo():']
        compare_output(self, out, d, cmds)

        # # Test step!
        # cmds = ['step!', 'continue']
        # d = strarray_setup(cmds)
        # d.core.start()
        # ##############################
        # x = 5
        # try:
        #     y = 2
        #     z = 1/0
        # except:
        #     pass
        # ##############################
        # d.core.stop(options={'remove': True})
        # out = ['-- x = 5',
        #        '!! z = 1/0\n']
        # compare_output(self, out, d, cmds)

        # Test "step" with sets of events. Part 1
        cmds = ['step call exception',
                'step call exception', 'continue']
        d = strarray_setup(cmds)
        d.core.start()
        ##############################
        x = 5  # NOQA
        try:
            def foo1():
                """
                Returns the two - dimensional integers.

                Args:
                """
                y = 2  # NOQA
                raise Exception
                return
            foo1()
        except:
            pass
        z = 1  # NOQA
        # ##############################
        # d.core.stop(options={'remove': True})
        # out = ['-- x = 5',
        #        '-> def foo1():',
        #        '!! raise Exception']
        # compare_output(self, out, d, cmds)

        # # Test "step" will sets of events. Part 2
        # cmds = ['step call exception 1+0',
        #         'step call exception 1', 'continue']
        # d = strarray_setup(cmds)
        # d.core.start()
        # ##############################
        # x = 5
        # try:
        #     def foo2():
        #         y = 2
        #         raise Exception
        #         return
        #     foo2()
        # except:
        #     pass
        # z = 1
        # ##############################
        # d.core.stop(options={'remove': True})
        # out = ['-- x = 5',
        #        '-> def foo2():',
        #        '!! raise Exception']
        # compare_output(self, out, d, cmds)

        return

    @unittest.skip("Need to fix")
    def test_step_between_fn(self):
        """
        Generate a function to run.

        Args:
            self: (todo): write your description
        """

        # Step into and out of a function
        def sqr(x):
            """
            Sqr ( x ) of x.

            Args:
                x: (array): write your description
            """
            return x * x
        for cmds, out, eventset in (
            (['step', 'step', 'continue'],
             ['-- x = sqr(4)   # NOQA',
              '-- return x * x',
              '-- y = 5  # NOQA'],
             frozenset(('line',))),
            (['step', 'step', 'step', 'step', 'continue'],
             ['-- d.core.start()',
              '-- x = sqr(4)   # NOQA',
               '-> def sqr(x):',
               '-- return x * x',
               '<- return x * x'],
             tracer.ALL_EVENTS), ):
            d = strarray_setup(cmds)
            d.settings['events'] = eventset
            d.core.start()
            ##############################
            x = sqr(4)   # NOQA
            y = 5  # NOQA
            ##############################
            d.core.stop(options={'remove': True})
            compare_output(self, out, d, cmds)
            pass
        return

    @unittest.skip("Need to fix")
    def test_step_in_exception(self):
        """
        Runs : meth : class : xcmd.

        Args:
            self: (todo): write your description
        """

        def boom(x):
            """
            Returns true if x is a boolean value.

            Args:
                x: (int): write your description
            """
            y = 0/x  # NOQA
            return

        def bad(x):
            """
            Badomposition.

            Args:
                x: (todo): write your description
            """
            boom(x)
            return x * x
        cmds = ['step', 'step', 'step', 'step', 'step', 'step',
                'step', 'step', 'step', 'step', 'continue']
        d = strarray_setup(cmds)
        try:
            d.core.start()
            x = bad(0)  # NOQA
            self.assertTrue(False, 'should have raised an exception')
        except ZeroDivisionError:
            self.assertTrue(True, 'Got the exception')
            pass
        d.core.stop(options={'remove': True})

        out = ['-- x = bad(0)  # NOQA', # line event
               '-> def bad(x):',        # call event
               '-- boom(x)',            # line event
               '-> def boom(x):',       # call event
               '-- y = 0/x  # NOQA',    # line event
               '!! y = 0/x  # NOQA',    # exception event
               '<- y = 0/x  # NOQA',    # return event
               '!! boom(x)',            # exception event
               '<- boom(x)',            # return event
               '!! x = bad(0)  # NOQA', # exception event
               '-- except ZeroDivisionError:']
        compare_output(self, out, d, cmds)
        return

    pass

if __name__ == '__main__':
    unittest.main()
    pass
