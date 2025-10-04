
import numpy
import math

import numpy
import math

def S_inv_eulerZYX_body_deriv(euler_coordinates, omega):
    y = euler_coordinates[1]
    z = euler_coordinates[2]

    J_y = numpy.zeros((3, 3))
    J_z = numpy.zeros((3, 3))

    J_y[0, 1] = math.tan(y)/math.cos(y)*math.sin(z)
    J_y[0, 2] = math.tan(y)/math.cos(y)*math.cos(z)
    J_y[2, 1] = math.sin(z)/(math.cos(y))**2
    J_y[2, 2] = math.cos(z)/(math.cos(y))**2

    J_z[0, 1] = math.cos(z)/math.cos(y)
    J_z[0, 2] = -math.sin(z)/math.cos(y)
    J_z[1, 1] = -math.sin(z)
    J_z[1, 2] = -math.cos(z)
    J_z[2, 1] = math.cos(z)*math.tan(y)
    J_z[2, 2] = -math.sin(z)*math.tan(y)

    J = numpy.zeros((3, 3))
    J[:, 1] = numpy.dot(J_y, omega)
    J[:, 2] = numpy.dot(J_z, omega)

    return J