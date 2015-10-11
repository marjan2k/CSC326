cache = { 0: 0, 1: 1 }
def fib(n, l):
    l.append(n)
    if (n not in cache):
        cache[n] = fib(n-1, l) + fib(n-2, l)
    return cache[n]
