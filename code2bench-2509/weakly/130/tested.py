from scipy.spatial.transform import Rotation as R
import numpy as np

def align_vector_sets(vec_set1: np.ndarray, vec_set2: np.ndarray) -> np.ndarray:
    # Compute the optimal rotation using Kabsch algorithm
    centroid1 = np.mean(vec_set1, axis=0)
    centroid2 = np.mean(vec_set2, axis=0)
    
    # Center the vectors
    vec_set1_centered = vec_set1 - centroid1
    vec_set2_centered = vec_set2 - centroid2
    
    # Compute the covariance matrix
    cov_matrix = np.dot(vec_set1_centered.T, vec_set2_centered)
    
    # Compute the optimal rotation using SVD
    u, s, vh = np.linalg.svd(cov_matrix)
    rotation_matrix = np.dot(u, vh)
    
    # Ensure a proper rotation (det(rotation_matrix) == 1)
    if np.linalg.det(rotation_matrix) < 0:
        vh[:, -1] *= -1
        rotation_matrix = np.dot(u, vh)
    
    # Convert rotation matrix to quaternion
    rotation = R.from_matrix(rotation_matrix)
    quaternion = rotation.as_quat()
    
    # Normalize the quaternion
    quaternion = quaternion / np.linalg.norm(quaternion)
    
    return quaternion