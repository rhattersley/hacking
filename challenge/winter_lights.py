#!/usr/bin/env python3

# https://codility.com/programmers/task/winter_lights/
from spans import solution as span_solution


def reference(S):
    def is_palindrome_anagram(S):
        import collections
        counts = collections.Counter(S)
        num_odd = len([count for count in counts.values() if count % 2 == 1])
        num_even = len([count for count in counts.values() if count % 2 == 0])
        return num_odd < 2
    subsequences = []
    for n in range(1, len(S) + 1):
        subsequences.extend(S[i:i+n] for i in range(len(S)-n+1))
    valid_subsequences = filter(is_palindrome_anagram, subsequences)
    return len(list(valid_subsequences))


def check(S, expected=None):
    if expected is None:
        expected = reference(S)
    import time
    t = time.time()
    result = span_solution(S)
    t2 = time.time()
    print('Done in {} s'.format(t2 - t))
    if result == expected:
        print(' OK ({})'.format(result))
    else:
        print(' ERROR\n   Expected {}, got {}'.format(expected, result))
        exit()


if __name__ == '__main__':
    #check('0' * 200, 0)
    if 1:
        Ss = ['000', '0001', '00011', '000110', '0001100', '00011000',
              '000110001', '0001100011', '00011000110', '000110001100']
        #Ss = ['000110001']
        for S in Ss:
            check(S)
    if 0:
        check('00110', 13)
        check('100101', 15)
        check('01001', 11)
        check('112', 5)
        check('113', 5)
        check('9999', 10)
        check('9998', 8)
        check('9989', 7)
        check('9987', 6)
        check('998', 5)
        check('02002', 11)
        check('0', 1)
        check('1', 1)
        check('00', 3)
        check('01', 2)
        check('000', 6)
        check('001', 5)
        check('010', 4)
        check('100', 5)
        check('012', 3)
        check('0000', 10)
    if 0:
        import itertools
        for S in itertools.product('0123456789', repeat=4):
            S = ''.join(S)
            check(S)
