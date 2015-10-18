import math

def factorize(n):
    """ Takes an integer N and returns an ordered list of prime integers
    whose product equals to N.
    >>> factorize(1)
    [1]
    >>> factorize(6)
    [1, 2, 3]
    >>> factorize(12)
    [1, 2, 2, 3]
    >>> factorize(0)
    Traceback (most recent call last):
        ...
    ValueError: n cannot be 0
    >>> factorize(-6)
    [-1, 2, 3]
    """
    # 0 cannot be prime factorized
    if n == 0:
        raise ValueError("n cannot be 0")
    # 1 is a prime factor for all positive ints, -1 is a prime factor for negative ints
    factors = [1 if n > 0 else -1]
    # Convert to positive integer to calculate prime factors if n is negative
    if n < 0:
        n = n * -1

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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
