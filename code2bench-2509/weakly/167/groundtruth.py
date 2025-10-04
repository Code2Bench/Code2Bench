
import numpy

import numpy

def logmap_so3(R):
    R11 = R[0, 0]
    R12 = R[0, 1]
    R13 = R[0, 2]
    R21 = R[1, 0]
    R22 = R[1, 1]
    R23 = R[1, 2]
    R31 = R[2, 0]
    R32 = R[2, 1]
    R33 = R[2, 2]
    tr = numpy.trace(R)
    omega = numpy.empty((3,), dtype=numpy.float64)

    if(numpy.abs(tr + 1.0) < 1e-10):
        if(numpy.abs(R33 + 1.0) > 1e-10):
            omega = (numpy.pi / numpy.sqrt(2.0 + 2.0 * R33)) * numpy.array([R13, R23, 1.0+R33])
        elif(numpy.abs(R22 + 1.0) > 1e-10):
            omega = (numpy.pi / numpy.sqrt(2.0 + 2.0 * R22)) * numpy.array([R12, 1.0+R22, R32])
        else:
            omega = (numpy.pi / numpy.sqrt(2.0 + 2.0 * R11)) * numpy.array([1.0+R11, R21, R31])
    else:
        magnitude = 1.0
        tr_3 = tr - 3.0
        if tr_3 < -1e-7:
            theta = numpy.arccos((tr - 1.0) / 2.0)
            magnitude = theta / (2.0 * numpy.sin(theta))
        else:
            magnitude = 0.5 - tr_3 * tr_3 / 12.0

        omega = magnitude * numpy.array([R32 - R23, R13 - R31, R21 - R12])

    return omega