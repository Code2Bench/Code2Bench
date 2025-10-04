import numpy as np

def j_mat(two_body_integrals: np.ndarray) -> np.ndarray:
    n = two_body_integrals.shape[0]
    j = np.zeros((n, n))
    for p in range(n):
        for q in range(n):
            j[p, q] = np.einsum('ijkl', two_body_integrals[p, q, p, q])
    return j