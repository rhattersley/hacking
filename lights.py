#!/usr/bin/env python
import collections
import itertools


DIGITS = range(3)


def count_snippets(digits):
    n_digits = len(digits)
    n_valid_snippets = 0
    for length in range(1, n_digits + 1):
        for start in range(0, n_digits + 1 - length):
            snippet = digits[start:start + length]
            counts = collections.Counter(snippet).values()
            n_odd = len([v for v in counts if v % 2 == 1])
            if n_odd < 2:
                n_valid_snippets += 1
    return n_valid_snippets


def show(digits):
    # (0, 1) -> (4, 5, 4, ...)
    state = [count_snippets(digits + (next_digit,)) for next_digit in DIGITS]
    formatted_state = ', '.join(map(lambda v: '{:2}'.format(v), state))
    print('{!s:<10} -> {}'.format(''.join(map(str, digits)), formatted_state))


def show_next(max_digits):
    for n_digits in range(max_digits + 1):
        for digits in itertools.product(range(2), repeat=n_digits):
            show(digits)


if __name__ == '__main__':
    show_next(4)
    if 0:
        show((0,))
        show((0, 0))
        show((0, 1))
        show((0, 0, 0))
        show((0, 0, 1))
        show((0, 1, 0))
        show((0, 1, 1))
