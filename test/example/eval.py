def five():
    """
    Return a function that returns a list of the last call.

    Args:
    """
    return 5
a = '1'
eval_str = a + '*2'
x = eval(eval_str)
x = eval('five()')
exec_str = 'x = 30'
exec(exec_str)
print(x)
