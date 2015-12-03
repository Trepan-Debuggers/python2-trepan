def foo(a, **options):
    bar(a, **options)
    options = {'c': 5, 'b': 10}
    bar(a, **options)

def bar(a, b=1, c=2):
    print "a, b, c= ", a, b, c

foo(5, b=1, c=2)
