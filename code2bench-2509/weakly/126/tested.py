from scipy.spatial.transform import Rotation as R
import numpy as np

def euler2quat(euler: np.ndarray) -> np.ndarray:
    assert euler.shape == (3,), "Input array must have shape (3,)"
    rotation = R.from_euler('xyz', euler, degrees=False)
    quat = rotation.as_quat()
    return np.array(quat)