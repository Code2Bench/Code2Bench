from typing import List
import numpy as np

def get_c2w(w2cs: List[np.ndarray], transform_matrix: np.ndarray, relative_c2w: bool = True) -> np.ndarray:
    if relative_c2w:
        c2w = [np.linalg.inv(w2c) for w2c in w2cs]
        c2w = [np.dot(c2w[0], c2w[i]) for i in range(len(c2w))]
    else:
        c2w = [np.linalg.inv(w2c) for w2c in w2cs]
    c2w = [np.dot(transform_matrix, c2w[i]) for i in range(len(c2w))]
    return np.array(c2w, dtype=np.float32)