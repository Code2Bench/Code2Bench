import numpy as np

def _first_divided_difference(
    d: np.ndarray, 
    fct: Callable, 
    fctder: Callable, 
    atol: float = 1e-12, 
    rtol: float = 1e-12
) -> np.ndarray:
    n = len(d)
    result = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                result[i, j] = fctder(d[i])
            else:
                if np.isclose(d[i], d[j], atol=atol, rtol=rtol):
                    result[i, j] = fctder(d[i])
                else:
                    result[i, j] = (fct(d[i]) - fct(d[j])) / (d[i] - d[j])
    return result