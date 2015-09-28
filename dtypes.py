"""

    >>> a = Array([1, 2.2], dtype=Float32)
    >>> a
    Array([1.0, 2.200000047683716], dtype=Float32)
    >>> a[0]
    1.0
    >>> type(a[0])
    Float32

    >>> times = Array(['2015-02-30T00:00:00'], dtype=Datetime360)
    >>> times
    Array([2015-02-30T00:00:00], dtype=Datetime360)
    >>> str(times[0])
    '2015-02-30T00:00:00'
    >>> repr(times[0])
    'Datetime360(2015-02-30T00:00:00)'
    >>> type(times[0])
    Datetime360

    Parameterised types (e.g. categoricals, custom calendars, physical units)
    need a new class for each set of parameters.
    => Need a factory function that builds classes at runtime.

    categories = Array(['a', 'b', 'c', 'a'], dtype=categories('abc'))

    TODO: Physical units should have an underlying dtype?
        e.g. Unit(Float32, 'm.s-1')

        Would/should there be anything to stop you doing something odd like:
            Unit(Datetime360, 'm.s-1')
        or:
            Unit(Unit(Float32, 'm'), 's')
        A class hierarchy with Number in the mix?

    >>> speeds = Array([1, 2.5], dtype=Unit('m.s-1'))
    >>> speeds
    Array([1.0, 2.5], dtype=Unit('m.s-1'))
    >>> mag = speeds * speeds
    >>> mag
    Array([1.0, 6.25], dtype=Unit('m2.s-2'))

"""
import struct

import numpy as np


class Array(object):
    def __init__(self, values, dtype):
        self._packed_values = [dtype.pack(v) for v in values]
        self.dtype = dtype

    def __len__(self):
        return len(self._packed_values)

    def __repr__(self):
        values = [str(self.dtype.unpack(pv)) for pv in self._packed_values]
        return 'Array([{}], dtype={})'.format(', '.join(values), self.dtype)

    def __getitem__(self, indices):
        result = self._packed_values[indices]
        if isinstance(indices, int):
            result = self.dtype.unpack(result)
        return result

    def __mul__(self, other):
        values = []
        for i in range(len(self)):
            values.append(self[i] * other[i])
        return Array(values, self.dtype * other.dtype)


class DTypeMeta(type):
    def __repr__(cls):
        return cls.__name__


class DType(object):
    __metaclass__ = DTypeMeta


class Float32(DType):
    @classmethod
    def pack(cls, value):
        """Return the bytes corresponding to a Python object."""
        return struct.pack('f', float(value))

    # Make a new instance from a packed representation.
    @classmethod
    def unpack(cls, packed_value):
        value, = struct.unpack('f', packed_value)
        return cls(value)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)


class Datetime360(DType):
    @classmethod
    def pack(cls, value):
        """Return the bytes corresponding to a Python object."""
        date, _ = value.split('T')
        year, month, day = map(int, date.split('-'))
        return struct.pack('l', (year*12 + (month-1))*30 + (day-1))

    # Make a new instance from a packed representation.
    @classmethod
    def unpack(cls, packed_value):
        days, = struct.unpack('l', packed_value)
        day = days % 30 + 1
        month = days // 30 % 12 + 1
        year = days // 360
        value = '{:04}-{:02}-{:02}T00:00:00'.format(year, month, day)
        return cls(value)

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return self._value

    def __repr__(self):
        return 'Datetime360({})'.format(self._value)


class UnitMeta(DTypeMeta):
    def __repr__(cls):
        return '{}({!r})'.format(cls.__name__, cls._unit)

    def __mul__(cls1, cls2):
        def bits(unit):
            import collections
            us = collections.Counter()
            for u in unit.split('.'):
                n = int(u[1:]) if u[1:] else 1
                us[u[0]] = n
            return us
        b1 = bits(cls1._unit)
        b2 = bits(cls2._unit)
        b1.update(b2)
        u = '.'.join(k + str(b1[k]) for k in sorted(b1.keys()))
        return Unit(u)


def Unit(unit):
    class Unit(DType):
        __metaclass__ = UnitMeta
        _unit = unit
        @classmethod
        def pack(cls, value):
            return struct.pack('f', float(value))

        @classmethod
        def unpack(cls, packed_value):
            value, = struct.unpack('f', packed_value)
            return cls(value)

        def __init__(self, value):
            self.value = value

        def __repr__(self):
            return repr(self.value)

        def __mul__(self, other):
            return self.value * other.value

    return Unit
