def rotate_word(str, i):
    for j in xrange(0, i):
        str = str[1:] + str[0]
    return str
