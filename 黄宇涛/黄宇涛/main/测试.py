class a:
    def __init__(self):
        self.x = 0
    def update(self):
        self.x += 1
s = [1, 2, 3]
class b:
    def __init__(self, a):
        self.a = a
    def update(self):
        s[0] = 10
        print(s)

A = a()
B = b(A)
while True:
    A.update()
    B.update()


