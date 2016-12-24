.. _set_substitute:

Set Substitute
--------------
**set substitute** **from-name** **to-path*

Add a substitution rule replacing FROM into TO in source file names.
If a substitution rule was previously set for FROM, the old rule
is replaced by the new one.

Spaces in "filesnames" like <frozen importlib._bootstrap> messes up our normal shell
tokenization, so we have added a hack to ignore <frozen .. >.

So for frozen files like <frozen importlib._bootstrap>, use importlib._bootstrap

Examples:
++++++++

    set substitute importlib._bootstrap /usr/lib/python3.4/importlib/_bootstrap.py
    set substitute ./gcd.py /tmp/gcd.py

See also:
+++++++++
`show substitute`