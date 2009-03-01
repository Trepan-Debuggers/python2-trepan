#!/usr/bin/env python
'Unit test for pydbg.io.tcp*'
import inspect, os, sys, unittest

from import_relative import *
import_relative('io', '...pydbg', 'pydbg')
Mserver   = import_relative('io.tcpserver', '...pydbg', 'pydbg')
Mclient   = import_relative('io.tcpclient', '...pydbg', 'pydbg')
import_relative('interface', '...pydbg', 'pydbg')
Mcomcodes = import_relative('interface.comcodes', '...pydbg', 'pydbg')

class TestTCP(unittest.TestCase):
    """Tests TCPServer and TCPClient"""

    def test_client_server(self):
        server = Mserver.TCPServer(opts={'open': True})
        client = Mclient.TCPClient(opts={'open': True})
        for line in ['one', 'two', 'three']: 
            server.writeline(line)
            self.assertEqual(line, client.read_msg().rstrip('\n'))
            pass
        for line in ['four', 'five', 'six']: 
            client.writeline(line)
            self.assertEqual(line, server.read_msg().rstrip('\n'))
            pass
        return

if __name__ == '__main__':
    unittest.main()
