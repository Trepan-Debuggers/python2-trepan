Running
=======

Running the program.

Step, Next, Finish, Skip, Retval
--------------------------------

Here's a sample session using these commands:

.. code:: python

        (trepan2) set basename  # Short filenames in display
        (trepan2) set trace  # Show the events
        (trepan2) step 4
        line - gcd.py:13
        line - gcd.py:26
        line - gcd.py:40
        line - gcd.py:41
        (gcd.py:41): <module>
        ** 41     check_args()
        (trepan2) s # 's' is an abbreviation for step
        call - gcd.py:13
        (gcd.py:13): check_args
        -> 13 def check_args():
        (trepan2) step<   # Step until the next return
        line - gcd.py:14
        line - gcd.py:17
        line - gcd.py:18
        line - gcd.py:19
        line - gcd.py:17
        line - gcd.py:18
        line - gcd.py:19
        line - gcd.py:17
        return - gcd.py:17
        (gcd.py:17): check_args
        <- 17     for i in range(2):
        (trepan2) set trace off # That's enough tracing
        (trepan2) next  # like step but skips over function calls
        (gcd.py:43): <module>
        ** 43     (a, b) = sys.argv[1:3]
        (trepan2) # A carriage-return or empty command runs the last step/next
        (gcd.py:44): <module>
        ** 44     print "The GCD of %d and %d is %d" % (a, b, gcd(a, b))
        (trepan2) s<  # step until the next call
        (gcd.py:26): gcd
        -> 26 def gcd(a,b):
        (trepan2) finish  # run until return of *this* function; compare with s<
        (gcd.py:38): gcd
        <- 38     return gcd(b-a, a)
        (trepan2) retval  # show the return value
          1
        (trepan2)
