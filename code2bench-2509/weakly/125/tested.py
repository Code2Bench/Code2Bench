from scipy.spatial.transform import Rotation as R
import numpy as np

def mat2quat(rmat: np.ndarray) -> np.ndarray:
    rotation = R.from_matrix(rmat)
    quat = rotation.as_quat()
    return np.array(quat)