#!/usr/bin/env python
import inspect, unittest, sys
from fn_helper import compare_output, strarray_setup


class TestJump(unittest.TestCase):
    def test_jump(self):
        """
        Determine test test.

        Args:
            self: (todo): write your description
        """
        # FIXME
        return

        if sys.version_info[0] == 2 and sys.version_info[1] <= 4:
            print("skipping jump test on Python 2.4")

        # See that we can jump with line number
        curframe = inspect.currentframe()
        cmds = ['step',
                'jump %d' % (curframe.f_lineno+8),
                'continue']                     # 1
        d = strarray_setup(cmds)                # 2
        d.core.start()                          # 3
        ##############################          # 4...
        x = 5
        x = 6
        x = 7
        z = 8  # NOQA
        ##############################
        d.core.stop(options={'remove': True})
        out = ['-- x = 5',  # x = 10 is shown in prompt, but not run.
               '-- x = 6',
               '-- z = 8']
        compare_output(self, out, d, cmds)
        self.assertEqual(5, x)  # Make sure x = 6, 7 were skipped.
        return
    pass

if __name__ == '__main__':
    unittest.main()
