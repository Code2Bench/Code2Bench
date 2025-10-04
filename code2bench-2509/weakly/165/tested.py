import numpy as np

def unskew(R: np.ndarray) -> np.ndarray:
    return np.array([R[2, 1], R[0, 2], R[1, 0]], dtype=np.float64)