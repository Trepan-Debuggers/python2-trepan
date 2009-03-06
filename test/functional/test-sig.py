#!/usr/bin/env python
import os, signal, unittest
import tracer
from fn_helper import strarray_setup, compare_output

class TestSigHandler(unittest.TestCase):

    def test_handle(self):

        # See that we handle a USR1 signal with a 'stop' action
        cmds = ['handle usr1 stop', 'continue', 'where', 'continue']
        d = strarray_setup(cmds)
        d.core.start()
        ##############################
        x = 5
        os.kill(os.getpid(), signal.SIGUSR1)
        y = 6
        ##############################
        d.core.stop()
        out = ['-- x = 5',
               "-- y = 6\n     called from file 'test-sig.py' at line 17"]
        compare_output(self, out, d, cmds)


        # How about USR2 signal with 'ignore' and 'noprint' actions?
        cmds = ['handle usr2 ignore nopass noprint', 
                'continue']
        d = strarray_setup(cmds)
        d.core.start()
        ##############################
        x = 7
        os.kill(os.getpid(), signal.SIGUSR2)
        y = 8
        ##############################
        d.core.stop()
        out = ['-- x = 7']
        compare_output(self, out, d, cmds)

        return

    pass

if __name__ == '__main__':
    unittest.main()
    pass





