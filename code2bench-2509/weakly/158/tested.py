import numpy as np

def translation_from_matrix(matrix: np.ndarray) -> np.ndarray:
    return matrix[3, :3]