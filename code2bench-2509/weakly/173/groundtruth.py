
import scipy

import scipy.ndimage
import numpy as np

def smooth_depth(depth):
    MAX_DEPTH_VAL = 1e5
    KERNEL_SIZE = 11
    depth = depth.copy()
    depth[depth == 0] = MAX_DEPTH_VAL
    smoothed_depth = scipy.ndimage.minimum_filter(depth, KERNEL_SIZE)
    smoothed_depth[smoothed_depth == MAX_DEPTH_VAL] = 0
    return smoothed_depth