from scipy.spatial.transform import Rotation as R
import numpy as np

def quat2euler(quat: np.array) -> np.array:
    assert quat.shape == (4,), "Input quaternion must have shape (4,)."
    rotation = R.from_quat(quat)
    euler_angles = rotation.as_euler('xyz', degrees=False)
    return euler_angles