#!/usr/bin/env python
'Unit test for pydbgr.io.tcp*'
import os
if hasattr(os, 'mkfifo'):

    import inspect, sys, unittest

    from import_relative import *
    Mserver = import_relative('io.fifoserver', '...pydbgr')
    Mclient = import_relative('io.fifoclient', '...pydbgr')

    class TestFIFO(unittest.TestCase):
        """Tests FIFOServer and FIFOClient"""

        def test_client_server(self):
            server = Mserver.FIFOServer(opts={'open': True})
            client = Mclient.FIFOClient(opts={'open': os.getpid()})
            self.assertTrue(True, 'FIXME: need to add a test here.')
            # FIXME need to use threading or forking
    #         for line in ['one', 'two', 'three']: 
    #             server.writeline(line)
    #             self.assertEqual(line, client.readline())
    #             pass
    #         for line in ['four', 'five', 'six']: 
    #             client.writeline(line)
    #             self.assertEqual(line, server.readline())
    #             pass
            return

    if __name__ == '__main__':
        unittest.main()
        pass
    pass
