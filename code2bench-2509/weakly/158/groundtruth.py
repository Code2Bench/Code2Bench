
import numpy

import numpy as np

def translation_from_matrix(matrix) -> np.ndarray:
    return np.array(matrix, copy=False)[:3, 3].copy()