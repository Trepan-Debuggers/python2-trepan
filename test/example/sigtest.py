#!/usr/bin/env python
"""Something to use to test signal handling. Basically we just need
a program that installs a signal handler.
"""
import sys, os, signal, time
def signal_handler(num, f):
    # from pydbgr.api import debug; debug()
    f = open('log', 'w+')
    f.write('signal received\n')
    f.close()
    sys.exit(0)

# FIXME make debugger oblivious to this:
# signal.signal(signal.SIGUSR1, signal_handler)

if len(sys.argv) > 1 and sys.argv[1] == 'signal':
    os.kill(os.getpid(), signal.SIGUSR1)
    # We need a statement after the above kill so we can see if the
    # debugger stop works.
    pass  
else:
    print "pid %d" % os.getpid()
    print "Waiting in time.sleep(10) for signal USR1." 
    while True:
        time.sleep(10)
        print "Still waiting for signal USR1." 
        pass
    pass

