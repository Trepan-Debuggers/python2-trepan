import os, sys
from import_relative import *

import_relative('pydbg', '...', 'pydbg')
debugger     = import_relative('debugger', '...pydbg', 'pydbg')
Mstringarray = import_relative('io.stringarray', '...pydbg', 'pydbg')

def strarray_setup(debugger_cmds):
    ''' Common setup to create a debugger with stringio attached '''
    stringin               = Mstringarray.StringArrayInput(debugger_cmds)
    stringout              = Mstringarray.StringArrayOutput()
    d_opts                 = {'input' : stringin, 
                              'output': stringout}
    d                      = debugger.Debugger(d_opts)
    d.settings['basename'] = True
    d.settings['different'] = False
    d.settings['autoeval'] = False
    return d

import re
pydbg_prompt = re.compile(r'^.. \d+.*\n\(Pydbg\) ')
pydbg_loc    = re.compile(r'^\(.+:\d+\): ')
def filter_line_cmd(a):
    '''Return output with source lines prompt and command removed'''
    # Next remove line locations and extra leading spaces.
    # For example:
    # -- 42         y = 5
    # becomes
    # -- y = 5
    a1 = [re.sub(r'^(..) \d+\s+', r'\1 ', s) for s in a
         if re.match(pydbg_prompt, s)]
    # First remove debugger location lines. 
    # For example: 
    #  (Pydbg) (test-next.py:41): test_next_between_fn
    a2 = [re.sub(r'\n\(Pydbg\) .*', '', s) for s in a1]
    return a2


def compare_output(obj, right, d, debugger_cmds):
    got = filter_line_cmd(d.intf[-1].output.output)
    if got != right:
        for i in range(len(got)):
            if i < len(right) and got[i] != right[i]:
                print "! ", got[i]
            else:
                print "  ", got[i]
                pass
            pass
        print '-' * 10
        for i in range(len(right)):
            if i < len(got) and got[i] != right[i]:
                print "! ", right[i]
            else:
                print "  ", right[i]
                pass
            pass
        pass
    obj.assertEqual(right, got)
    return

