class WordIterator(object):
    def __init__(self, file):
        self.file_iter = open(file, "r")
        self.words = []

    def __iter__(self):
        'Returns itself as an iterator object'
        return self

    def next(self):
        'Returns the next value till current is lower than high'
        if len(self.words) > 0:
            return self.words.pop(0)
        else:
            line = self.file_iter.next()
            self.words = line.split()
            return self.next()

def find_popular(file_name):
    word_count = {}
    it = WordIterator(file_name)
    for word in it:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    sorted_words = sorted(word_count.items(), reverse=True, key=lambda x: x[1])
    return [word[0] for word in sorted_words[:10]]

if __name__ == "__main__":
    print find_popular("test.txt")
