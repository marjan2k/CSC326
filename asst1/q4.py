import math

def factorize(n):
    factors = [1]
    while (n % 2 == 0):
        factors.append(2)
        n = n/2

    for i in xrange(3, int(math.ceil(math.sqrt(n))), 2):
        if (n % i == 0):
            factors.append(i)
            n = n/i

    # In the case n is a prime number greater than 2
    if (n > 2):
        factors.append(n)

    return factors
