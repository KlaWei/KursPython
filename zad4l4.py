from collections import Counter


class Words:
    def __init__(self, file):
        self.file = file

    def __iter__(self):
        return self

    def __next__(self):

        beginning = ""

        for line in self.file.readlines():
            line = line.strip()
            words = line.split()
            if words:
                words[0] = beginning + words[0]
                if line[-1:] == '-':
                    beginning = words[-1][:-1]
                    del words[-1]
                else:
                    beginning = ""
                for word in words:
                    word = word.strip(",.;“”:’?!\"()")
                    if word != "":
                        return word
        StopIteration()


def words(file):
    beginning = ""

    for line in file.readlines():
        line = line.strip()
        words = line.split()
        if words:
            words[0] = beginning + words[0]
            if line[-1:] == '-':
                beginning = words[-1][:-1]
                del words[-1]
            else:
                beginning = ""
            for word in words:
                word = word.strip(",.;“”:’?!\"()")
                if word != "":
                    yield word


def stats(filename):
    words_l = list()
    with open(filename) as input_file:
        for word in words(input_file):
            words_l.append(word)

    stat = [len(i) for i in words_l]
    return Counter(stat)


if __name__ == "__main__":
    filename = 'tale.txt'
    with open(filename) as input_file:
        for word in words(input_file):
            print(word)
    print(stats(filename))

    with open(filename) as input_file:
        print('iterator:')
        for w in Words(input_file):
            print(str(w))
