import numpy as np

def translation_matrix(direction: np.ndarray) -> np.ndarray:
    matrix = np.eye(4)
    matrix[:3, 3] = direction
    return matrix