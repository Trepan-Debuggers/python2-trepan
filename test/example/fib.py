#!/usr/bin/env python
import sys
def fib(n):
    if n <= 1: return 1
    return fib(n-1) + fib(n-2)
arg=int(sys.argv[1])
print("fib({})={}".format(arg, fib(arg)))
