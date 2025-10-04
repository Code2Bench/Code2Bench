import numpy as np
import math

def S_inv_eulerZYX_body_deriv(euler_coordinates: np.ndarray, omega: np.ndarray) -> np.ndarray:
    roll, pitch, yaw = euler_coordinates
    omega_x, omega_y, omega_z = omega
    
    # Construct J_y matrix for pitch
    J_y = np.array([
        [math.cos(pitch), 0, -math.sin(pitch)],
        [0, 1, 0],
        [math.sin(pitch), 0, math.cos(pitch)]
    ])
    
    # Construct J_z matrix for yaw
    J_z = np.array([
        [math.cos(yaw), -math.sin(yaw), 0],
        [math.sin(yaw), math.cos(yaw), 0],
        [0, 0, 1]
    ])
    
    # Compute the derivative of the inverse transformation matrix
    derivative = np.dot(np.dot(J_z, J_y), omega)
    
    return derivative