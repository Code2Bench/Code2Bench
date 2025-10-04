from scipy.spatial.transform import Rotation as R
import numpy as np

def mat2euler_intrinsic(rmat: np.ndarray) -> np.ndarray:
    rot = R.from_matrix(rmat)
    euler_angles = rot.as_euler('xyz', degrees=False)
    return np.array(euler_angles)