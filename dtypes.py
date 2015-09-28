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

    #>>> a = Array([1, 2.2], dtype=Float(32, endian='little'))
    #>>> a
    #array([1.0, 2.2], dtype=Float32(32, 'little'))
    #>>> a[0]
    #1.0
    #>>> type(a[0])
    #Float32

"""

import numpy as np


class Array(object):
    def __init__(self, values, dtype):
        self._packed_values = [dtype.pack(v) for v in values]
        self.dtype = dtype

    def __repr__(self):
        values = [str(self.dtype.unpack(pv)) for pv in self._packed_values]
        return 'Array([{}], dtype={})'.format(', '.join(values), self.dtype)

    def __getitem__(self, indices):
        result = self._packed_values[indices]
        if isinstance(indices, int):
            result = self.dtype.unpack(result)
        return result


class DtypeMeta(type):
    def __repr__(cls):
        return cls.__name__


class DType(object):
    __metaclass__ = DtypeMeta


class Float32(DType):
    @classmethod
    def pack(self, value):
        """Return the bytes corresponding to a Python object."""
        import struct
        return struct.pack('f', float(value))

    # Make a new instance from a packed representation.
    @classmethod
    def unpack(cls, packed_value):
        import struct
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
        import struct
        return struct.pack('l', (year*12 + (month-1))*30 + (day-1))

    # Make a new instance from a packed representation.
    @classmethod
    def unpack(cls, packed_value):
        import struct
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
