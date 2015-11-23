def my_map(func, iterable):
    return list(iterable) if func is None else [func(i) for i in iterable]

def my_reduce(func, iterable, initializer=None):
    iterable = iter(iterable)
    try:
        accum = iterable.next() if initializer is None else initializer
    except StopIteration:
        raise TypeError("my_reduce() of empty sequence with no initial value")
    for i in iterable:
        accum = func(accum, i)
    return accum

def my_filter(func, iterable):
    if func is None:
        result = [i for i in iterable if i]
    else:
        result = [i for i in iterable if func(i)]

    if type(iterable) == tuple:
        return tuple(result)
    elif type(iterable) == str:
        return "".join(result)
    return result

if __name__ == "__main__":
    print my_map(None, [1,2,3])
    print my_map(lambda x: x * 2, [])
    print my_map(lambda x: x + x, "abc")
    print my_map(lambda x: x + x, "")
    print my_map(lambda x: x * 2, [1,2,3])
    print my_map(lambda x: x * 2, (1,2,3))
    print my_map(lambda x: x * 2, set([1,2,3]))
    print my_map(lambda x: x, {'a': 5})

    print my_reduce(lambda x,y: x + y, {'a': 5})
    print my_reduce(lambda x,y: x + y, set(xrange(5)), 5)
    print my_reduce(lambda x,y: x + y, xrange(5))
    print my_reduce(lambda x,y: x + y, (0, 1, 2, 3, 4))

    print my_filter(None, xrange(5))
    print my_filter(lambda x: x % 2 == 0, [])

    print filter(None, "abc")
    print my_filter(None, "abc")
    print filter(None, "")
    print my_filter(None, "")
    print filter(lambda x: x, [])
    print my_filter(lambda x: x, [])
    print filter(None, xrange(5))
    print my_filter(None, xrange(5))
    print filter(lambda x: x % 2 == 0, (0, 1, 2, 3, 4))
    print my_filter(lambda x: x % 2 == 0, (0, 1, 2, 3, 4))
    print filter(lambda x: x % 2 == 0, xrange(5))
    print my_filter(lambda x: x % 2 == 0, xrange(5))
    print my_filter(lambda x: x % 2 == 0, xrange(5))
    print my_filter(lambda x: x % 2 == 0, set([0, 1, 2, 3, 4]))
