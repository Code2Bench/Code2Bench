
import numpy

import numpy

def unskew(R):
    return numpy.array([R[2, 1], R[0, 2], R[1, 0]], dtype=numpy.float64)