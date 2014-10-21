#!/usr/bin/env python
"""Something to use to test signal handling. Basically we just need
a program that installs a signal handler and sends it a signal.
"""
import os, signal, time
from trepan.api import debug; debug()

def signal_handler(num, f):
    print 'signal %d received' % num
    return

signal.signal(signal.SIGUSR1, signal_handler)
sleepy_time = 4
print "pid %d" % os.getpid()
print "Waiting in time.sleep(%d) for signal USR1."  % sleepy_time
while True:
    time.sleep(sleepy_time)
    os.kill(os.getpid(), signal.SIGUSR1)
    pass
pass
