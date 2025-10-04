import numpy as np

def first_order_rotation(rotvec: np.ndarray) -> np.ndarray:
    rot_matrix = np.eye(3)
    rot_matrix[0, 1] = -rotvec[2]
    rot_matrix[0, 2] = rotvec[1]
    rot_matrix[1, 0] = rotvec[2]
    rot_matrix[1, 2] = -rotvec[0]
    rot_matrix[2, 0] = -rotvec[1]
    rot_matrix[2, 1] = rotvec[0]
    return rot_matrix