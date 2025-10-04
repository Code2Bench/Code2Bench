from scipy.spatial.transform import Rotation as R
import numpy as np

def axisangle2quat(vec: np.array) -> np.array:
    rotation = R.from_rotvec(vec)
    quat = rotation.as_quat()
    return np.array(quat)