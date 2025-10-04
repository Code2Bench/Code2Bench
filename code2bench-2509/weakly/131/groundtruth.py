
from scipy.spatial.transform import Rotation as R

def mat2euler_intrinsic(rmat):
    """
    Converts given rotation matrix to intrinsic euler angles in radian.

    Parameters:
        rmat (np.array): 3x3 rotation matrix

    Returns:
        np.array: (r,p,y) converted intrinsic euler angles in radian vec3 float
    """
    return R.from_matrix(rmat).as_euler("XYZ")