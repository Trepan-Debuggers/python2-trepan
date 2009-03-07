#!/usr/bin/env python
"""Something to use to test signal handling. Basically we just need
a program that installs a signal handler and sends it a signal.
"""
import sys, os, signal, time
def signal_handler(num, f):
    # from pydbgr.api import debug; debug()
    print 'signal %d received' % num
    return

signal.signal(signal.SIGUSR1, signal_handler)
print "pid %d" % os.getpid()
print "Waiting in time.sleep(10) for signal USR1." 
while True:
    time.sleep(10)
    os.kill(os.getpid(), signal.SIGUSR1)
    pass
pass

