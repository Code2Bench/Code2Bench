import numpy as np
import math

def quaternion_from_matrix(matrix: np.ndarray, isprecise: bool = False) -> np.ndarray:
    if not isprecise:
        m = matrix
        trace = m[0, 0] + m[1, 1] + m[2, 2]
        if trace > 0:
            s = 0.5 / math.sqrt(trace)
            w = 0.5 / s
            x = (m[2, 1] - m[1, 2]) * s
            y = (m[0, 2] - m[2, 0]) * s
            z = (m[1, 0] - m[0, 1]) * s
        else:
            if m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
                s = 0.5 / math.sqrt(1 + m[0, 0] - m[1, 1] - m[2, 2])
                w = (m[2, 1] - m[1, 2]) * s
                x = 0.5 / s
                y = (m[0, 1] + m[1, 0]) * s
                z = (m[0, 2] + m[2, 0]) * s
            elif m[1, 1] > m[2, 2]:
                s = 0.5 / math.sqrt(1 + m[1, 1] - m[0, 0] - m[2, 2])
                w = (m[0, 2] - m[2, 0]) * s
                x = (m[0, 1] + m[1, 0]) * s
                y = 0.5 / s
                z = (m[1, 2] + m[2, 1]) * s
            else:
                s = 0.5 / math.sqrt(1 + m[2, 2] - m[0, 0] - m[1, 1])
                w = (m[1, 0] - m[0, 1]) * s
                x = (m[0, 2] + m[2, 0]) * s
                y = (m[1, 2] + m[2, 1]) * s
                z = 0.5 / s
        q = np.array([w, x, y, z], dtype=np.float64)
        if q[0] < 0:
            q *= -1
        return q
    else:
        m = matrix
        mat = np.array(m, dtype=np.float64)
        eigenvalues, eigenvectors = np.linalg.eig(mat.T @ mat)
        idx = np.argmax(eigenvalues)
        q = eigenvectors[:, idx]
        if q[0] < 0:
            q *= -1
        return q