def gcd(num1, num2):
    largest_divisor = num1 if num1 < num2 else num2
    for i in xrange(largest_divisor, 0, -1):
        if num1 % i == 0 and num2 % i == 0:
            return i
