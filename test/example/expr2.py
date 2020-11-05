class C(object):
    def __init__(self):
        """
        Initialize the instance

        Args:
            self: (todo): write your description
        """
        self.prev = [100] + range(3)
    def p(self, i):
        """
        Return the next item

        Args:
            self: (todo): write your description
            i: (int): write your description
        """
        return self.prev[i]

x = C()
y = x.p(x.p(x.p(3)))
prev = [100] + range(3)
x = prev[prev[prev[0]]]
print(x)
