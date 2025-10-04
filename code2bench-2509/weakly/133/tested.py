import numpy as np

def k_mat(two_body_integrals: np.ndarray) -> np.ndarray:
    n = two_body_integrals.shape[0]
    k_matr = np.zeros((n, n))
    for p in range(n):
        for q in range(n):
            for r in range(n):
                for s in range(n):
                    k_matr[p, q] += two_body_integrals[r, s, p, q] * two_body_integrals[r, s, q, p]
    return k_matr