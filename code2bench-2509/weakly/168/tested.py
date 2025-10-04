import numpy as np

def S_inv_eulerZYX_body(euler_coordinates: np.ndarray) -> np.ndarray:
    roll, pitch, yaw = euler_coordinates
    sin_roll = np.sin(roll)
    cos_roll = np.cos(roll)
    sin_pitch = np.sin(pitch)
    cos_pitch = np.cos(pitch)
    sin_yaw = np.sin(yaw)
    cos_yaw = np.cos(yaw)

    S_inv = np.array([
        [cos_pitch * cos_yaw, -sin_roll * sin_pitch * cos_yaw - cos_roll * sin_yaw, sin_roll * sin_yaw - cos_roll * sin_pitch * cos_yaw],
        [cos_pitch * sin_yaw, -sin_roll * sin_pitch * sin_yaw + cos_roll * cos_yaw, sin_roll * cos_yaw + cos_roll * sin_pitch * sin_yaw],
        [-sin_pitch, sin_roll * cos_pitch, cos_roll * cos_pitch]
    ])
    return S_inv