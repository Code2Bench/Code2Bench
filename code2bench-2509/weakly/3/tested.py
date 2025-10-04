from typing import Tuple, List
from math import ceil, sqrt

def make_shifted_720Pwindows_bysize(size: Tuple[int, int, int], num_windows: Tuple[int, int, int]) -> List[Tuple[slice, slice, slice]]:
    time, height, width = size
    num_time, num_height, num_width = num_windows
    
    # 720P resolution constraint (height and width)
    max_height_720p = 720
    max_width_720p = 1280
    
    # Calculate the scaling factors to fit within 720P
    scale_h = max_height_720p / height
    scale_w = max_width_720p / width
    
    # Ensure the scaled dimensions do not exceed 720P
    scale = min(scale_h, scale_w)
    
    # Scaled dimensions
    scaled_height = int(height * scale)
    scaled_width = int(width * scale)
    
    # Calculate the number of windows in each dimension based on scaled size
    num_time_windows = ceil(time / num_time)
    num_height_windows = ceil(scaled_height / num_height)
    num_width_windows = ceil(scaled_width / num_width)
    
    # Generate window slices for each dimension
    time_slices = [slice(i * num_time, (i + 1) * num_time) for i in range(num_time_windows)]
    height_slices = [slice(i * num_height, (i + 1) * num_height) for i in range(num_height_windows)]
    width_slices = [slice(i * num_width, (i + 1) * num_width) for i in range(num_width_windows)]
    
    # Combine slices into windows
    windows = []
    for t_slice in time_slices:
        for h_slice in height_slices:
            for w_slice in width_slices:
                windows.append((t_slice, h_slice, w_slice))
    
    return windows