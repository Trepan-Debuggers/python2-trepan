class C(object):
    def __init__(self):
        self.prev = [100] + range(3)
    def p(self, i):
        return self.prev[i]

x = C()
y = x.p(x.p(x.p(3)))
prev = [100] + range(3)
x = prev[prev[prev[0]]]
print(x)
