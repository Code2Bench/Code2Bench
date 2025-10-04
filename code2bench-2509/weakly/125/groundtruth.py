
from scipy.spatial.transform import Rotation as R

def mat2quat(rmat):
    """
    Converts given rotation matrix to quaternion.

    Args:
        rmat (np.array): (..., 3, 3) rotation matrix

    Returns:
        np.array: (..., 4) (x,y,z,w) float quaternion angles
    """
    return R.from_matrix(rmat).as_quat()