def f(x):
    return x + 1

def g(x):
    return x * 2


def fone(x): return f(x)
def gone(x): return g(x)

print(fone(4))
print(gone(4))