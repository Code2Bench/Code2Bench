
import numpy

import numpy as np

def S_inv_eulerZYX_body(euler_coordinates):
    """ Relates angular rates w to changes in eulerZYX coordinates.
    dot(euler) = S^-1(euler_coordinates) * omega
    Also called: rotation-rate matrix. (E in Lupton paper)
    cfo, 2015/08/13

    """
    y = euler_coordinates[1]
    z = euler_coordinates[2]
    E = np.zeros((3, 3))
    E[0, 1] = np.sin(z)/np.cos(y)
    E[0, 2] = np.cos(z)/np.cos(y)
    E[1, 1] = np.cos(z)
    E[1, 2] = -np.sin(z)
    E[2, 0] = 1.0
    E[2, 1] = np.sin(z)*np.sin(y)/np.cos(y)
    E[2, 2] = np.cos(z)*np.sin(y)/np.cos(y)
    return E