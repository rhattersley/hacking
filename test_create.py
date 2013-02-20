import blaze


def test_shape():
    a = blaze.zeros('2, 3, int32')
    b = blaze.Array([0]*6, a.datashape)
    assert str(a) == str(b)


def test_size():
    a = blaze.zeros('70, 768, 1024, float32') # ~210 MiB


if __name__ == '__main__':
    test_shape()
