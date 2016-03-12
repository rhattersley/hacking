from __future__ import print_function


class _Future(object):
    def __init__(self, function, args, kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        args = map(repr, self.args)
        args.extend('{}={!r}'.format(name, value)
                    for name, value in self.kwargs.iteritems())
        return '{}({})'.format(self.function.__name__, ', '.join(args))

    def result(self):
        if not hasattr(self, 'value'):
            def resolve(value):
                return value.result() if isinstance(value, _Future) else value

            args = [resolve(arg) for arg in self.args]
            kwargs = {name: resolve(value)
                      for name, value in self.kwargs.iteritems()}
            self.value = self.function(*args, **kwargs)
        return self.value


def plugin(function):
    from functools import wraps
    @wraps(function)
    def _function(*args, **kwargs):
        return _Future(function, args, kwargs)
    return _function


@plugin
def env(name, default=None):
    import os
    value = os.environ.get(name, default)
    print('Getting {} as {}'.format(name, value))
    return value


@plugin
def eq(a, b):
    return a == b


def test(expr, expected):
    print('Testing:', expr)
    result = expr.result()
    print('   result:', result)
    print('      ', 'OK' if result == expected else 'FAIL')


if 1:
    test(env('HOME'), '/home/richard')
    test(env('HOME_FOO', default='wibble'), 'wibble')
    test(env('HOME_FOO', default=env('HOME')), '/home/richard')
    test(eq('a', 'a'), True)
    test(eq('a', 'b'), False)
    test(eq(env('HOME'), '/home/richard'), True)
home = env('HOME')
test(eq(home, home), True)
