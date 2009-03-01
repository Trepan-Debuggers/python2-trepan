#!/usr/bin/env python
'Unit test for the debugger pydb.processor.cmdproc'
import os, sys, types, unittest
from import_relative import *

Mcmdproc = import_relative('processor.cmdproc', '...pydbg')

from cmdhelper import dbg_setup

class TestProcesor(unittest.TestCase):
    
    def setUp(self):
        self.d, self.cp = dbg_setup()
    
    def test_populate_commands(self):
        """ Test that we are creating instances for all of classes of files
        in the command directory ."""
        for i in self.cp.cmd_instances:
            self.assertEqual(types.TupleType, type(i.name_aliases), 
                             "not tuple %s." % repr(i.name_aliases))
            self.assertNotEqual(0, i.name_aliases, 
                                "tuple not be empty %s" % repr(i.name_aliases))
            self.assertEqual([],
                             [item for item in i.name_aliases 
                              if types.StringType != type(item)],
                             "elements of tuple should be strings %s" % 
                             repr(i.name_aliases))
            pass
        return

    def test_get_commands_aliases(self):
        "Test that the command processor finds a command, alias, and method"
        self.assertTrue('quit' in self.cp.name2cmd.keys())
        self.assertEqual('quit', self.cp.alias2name['q'])
        import inspect
        self.assertTrue(inspect.ismethod(self.cp.name2cmd['quit'].run))
        return

    def test_resolve_name(self):
        "Test that the command processor finds a command, alias, and method"
        self.assert_(Mcmdproc.resolve_name(self.cp, 'quit'))
        self.assert_(Mcmdproc.resolve_name(self.cp, 'q'))
        return

if __name__ == '__main__':
    unittest.main()
