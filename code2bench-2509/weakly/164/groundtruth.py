
import numpy

import numpy

def skew(v):
    """Returns the skew-symmetric matrix of a vector
    cfo, 2015/08/13

    """
    return numpy.array([[0, -v[2], v[1]],
                        [v[2], 0, -v[0]],
                        [-v[1], v[0], 0]], dtype=numpy.float64)