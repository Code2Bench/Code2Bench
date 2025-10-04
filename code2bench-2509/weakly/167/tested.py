import numpy as np

def logmap_so3(R: np.ndarray) -> np.ndarray:
    trace = np.trace(R)
    theta = np.arccos((trace - 1.0) / 2.0)
    threshold = 1e-10
    if abs(theta) < threshold:
        return np.zeros(3)
    elif abs(theta - np.pi) < threshold:
        theta = np.pi
        omega = (R - R.T) / (2 * np.sin(theta))
        return theta * omega
    else:
        omega = (R - R.T) / (2 * np.sin(theta))
        return theta * omega