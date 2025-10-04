
from scipy.spatial.transform import Rotation as R

def euler2quat(euler):
    """
    Converts extrinsic euler angles into quaternion form

    Args:
        euler (np.array): (r,p,y) angles

    Returns:
        np.array: (x,y,z,w) float quaternion angles

    Raises:
        AssertionError: [Invalid input shape]
    """
    return R.from_euler("xyz", euler).as_quat()