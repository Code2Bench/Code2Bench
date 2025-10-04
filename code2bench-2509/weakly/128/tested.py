from scipy.spatial.transform import Rotation as R
import numpy as np

def quat2axisangle(quat: np.array) -> np.array:
    rotation = R.from_quat(quat)
    axis_angle = rotation.as_rotvec()
    return axis_angle