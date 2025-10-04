import numpy as np

def quaternion_multiply(quaternion1: list | np.ndarray, quaternion0: list | np.ndarray) -> np.ndarray:
    w1, x1, y1, z1 = quaternion1
    w2, x2, y2, z2 = quaternion0
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w, x, y, z])