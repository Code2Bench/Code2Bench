
import numpy
import math

import numpy
import math

def orthogonalization_matrix(lengths, angles):
    """Return orthogonalization matrix for crystallographic cell coordinates.

    Angles are expected in degrees.

    The de-orthogonalization matrix is the inverse.

    >>> O = orthogonalization_matrix([10, 10, 10], [90, 90, 90])
    >>> numpy.allclose(O[:3, :3], numpy.identity(3, float) * 10)
    True
    >>> O = orthogonalization_matrix([9.8, 12.0, 15.5], [87.2, 80.7, 69.7])
    >>> numpy.allclose(numpy.sum(O), 43.063229)
    True

    """
    a, b, c = lengths
    angles = numpy.radians(angles)
    sina, sinb, _ = numpy.sin(angles)
    cosa, cosb, cosg = numpy.cos(angles)
    co = (cosa * cosb - cosg) / (sina * sinb)
    return numpy.array([[a * sinb * math.sqrt(1.0 - co * co), 0.0, 0.0, 0.0], [-a * sinb * co, b * sina, 0.0, 0.0],
                        [a * cosb, b * cosa, c, 0.0], [0.0, 0.0, 0.0, 1.0]])