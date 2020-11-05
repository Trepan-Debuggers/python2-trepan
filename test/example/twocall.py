def foo(a, **options):
    """
    Bar bar bar.

    Args:
        a: (todo): write your description
        options: (dict): write your description
    """
    bar(a, **options)
    options = {'c': 5, 'b': 10}
    bar(a, **options)

def bar(a, b=1, c=2):
    """
    Draw a bar.

    Args:
        a: (todo): write your description
        b: (todo): write your description
        c: (todo): write your description
    """
    print "a, b, c= ", a, b, c

foo(5, b=1, c=2)
