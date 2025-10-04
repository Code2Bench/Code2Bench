
from scipy.spatial.transform import Rotation as R

def quat2euler(quat):
    """
    Converts extrinsic euler angles into quaternion form

    Args:
        quat (np.array): (x,y,z,w) float quaternion angles

    Returns:
        np.array: (r,p,y) angles

    Raises:
        AssertionError: [Invalid input shape]
    """
    return R.from_quat(quat).as_euler("xyz")