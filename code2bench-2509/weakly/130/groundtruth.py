
from scipy.spatial.transform import Rotation as R

def align_vector_sets(vec_set1, vec_set2):
    """
    Computes a single quaternion representing the rotation that best aligns vec_set1 to vec_set2.

    Args:
        vec_set1 (np.array): (N, 3) tensor of N 3D vectors
        vec_set2 (np.array): (N, 3) tensor of N 3D vectors

    Returns:
        np.array: (4,) Normalized quaternion representing the overall rotation
    """
    rot, _ = R.align_vectors(vec_set1, vec_set2)
    return rot.as_quat()