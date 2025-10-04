import scipy.ndimage
import numpy as np

def smooth_depth(depth: np.ndarray) -> np.ndarray:
    depth[depth == 0] = 1e5
    smoothed_depth = scipy.ndimage.minimum_filter(depth, size=11)
    smoothed_depth[smoothed_depth == 1e5] = 0
    return smoothed_depth