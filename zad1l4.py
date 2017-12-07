#!/usr/bin/python3

import timeit
from math import sqrt


def primes_lc(n):
    return [x for x in range(2, n+1) if all(x % y != 0 for y in range(2, int(sqrt(x)) + 1))]


def primes_f(n):
    return list(filter(lambda x: all(x % y != 0 for y in range(2, int(sqrt(x)) + 1)), range(2, n + 1)))


def primes_it(n):
    primes = list()
    for x in range(2, n + 1):
        is_prime = True
        for y in range(2, int(sqrt(x)) + 1):
            if x % y == 0:
                is_prime = False
        if is_prime is True:
            primes.append(x)
    return primes


if __name__ == "__main__":
    print("\n       | funkcyjna | skladana | iterator ")
    iteracje = []
    for i in range(1, 101):
        skladana = timeit.timeit("primes_lc(%d)" % (i*100), setup="from __main__ import primes_lc",  number=1)
        funkcyjna = timeit.timeit("primes_f(%d)" % (i*100), setup="from __main__ import primes_f", number=1)
        iterator = timeit.timeit("primes_it(%d)" % (i*100), setup="from __main__ import primes_it", number=1)
        print("%6d | %9.5f | %8.5f | %8.5f" % (i*100, skladana, funkcyjna, iterator))
