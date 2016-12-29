import itertools


class Triple:
    def __init__(self, n, down, up):
        self.n = n
        self.up = up
        self.down = down

    @classmethod
    def from_n(cls, n):
        return cls(n, n // 2, (n + 1) // 2)

    def __repr__(self):
        return 'Triple({self.n}, {self.down}, {self.up})'.format(self=self)

    def __iadd__(self, other):
        self.n += other.n
        self.down += other.down
        self.up += other.up
        return self


class State:
    def __init__(self, n_symbols=10):
        self._n_symbols = n_symbols
        n_permutations = 1 << n_symbols
        self._n_permutations = n_permutations
        self._triples = [[Triple.from_n(0) for symbol in range(n_symbols)]
                            for i in range(n_permutations)]
        self._flips = 0

    def __repr__(self):
        lines = ['State:']
        for i in range(self._n_permutations):
            lines.append('{:0{n_symbols}b}: {}'.format(
                i, self[i], n_symbols=self._n_symbols))
        return '\n'.join(lines)

    def __getitem__(self, key):
        return self._triples[key ^ self._flips]

    def add_span(self, symbol, n_symbols):
        #print('Adding: {!r}'.format(symbol))
        assert isinstance(symbol, int)
        self[0][symbol] += Triple.from_n(n_symbols)

    def flip(self, i):
        self._flips ^= 1 << i


def solution(S):
    n_symbols = 10
    symbol_pairs = tuple(itertools.combinations(range(n_symbols), 2))
    # Running total for the number of valid subsequences.
    n_subsequences = 0
    # Current span
    current_symbol = -1
    n_current_symbols = 0
    state = State(n_symbols)
    for symbol in S:
        symbol = int(symbol)
        if symbol != current_symbol:
            if current_symbol != -1:
                state.add_span(symbol=current_symbol,
                               n_symbols=n_current_symbols)
            current_symbol = symbol
            n_current_symbols = 0
        n_current_symbols += 1
        state.flip(symbol)
        triples = state[0]
        # All even
        for triple in triples:
            n_subsequences += triple.n
        # One odd
        for symbol in range(n_symbols):
            triples = state[1 << symbol]
            for i, triple in enumerate(triples):
                if i == symbol:
                    n_subsequences += triple.n
                else:
                    n_subsequences += triple.down
        # Two odd
        for first, second in symbol_pairs:
            index = (1 << first) + (1 << second)
            triples = state[index]
            for i, triple in enumerate(triples):
                if i == first or i == second:
                    n_subsequences += triple.up
        n_subsequences += n_current_symbols
    return n_subsequences


if __name__ == '__main__':
    t = Triple.from_n(3)
    assert t.n == 3
    assert t.down == 1
    assert t.up == 2
    t = Triple.from_n(4)
    assert t.n == 4
    assert t.down == 2
    assert t.up == 2

    s = State(2)
    print(s)
    assert s[0][0].n == 0 and s[1][0].n == 2 and s[2][0].n == 4 and s[3][0].n == 6
    s.flip(0)
    assert s[0][0].n == 2 and s[1][0].n == 0 and s[2][0].n == 6 and s[3][0].n == 4
    s.flip(0)
    assert s[0][0].n == 0 and s[1][0].n == 2 and s[2][0].n == 4 and s[3][0].n == 6
    s.flip(1)
    assert s[0][0].n == 4 and s[1][0].n == 6 and s[2][0].n == 0 and s[3][0].n == 2
    s.flip(0)
    assert s[0][0].n == 6 and s[1][0].n == 4 and s[2][0].n == 2 and s[3][0].n == 0
    s.add_span(symbol=1, n_symbols=3)
    assert s[0][0].n == 6 and s[0][1].n == 10

    print('OK!')
