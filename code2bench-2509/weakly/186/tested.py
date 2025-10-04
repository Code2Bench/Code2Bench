import numpy as np

def post_process_sampled_indices(*, sampled_inds_list: list, attn_map: np.ndarray, image_size: int) -> tuple:
    inds = np.array([np.unravel_index(i, attn_map.shape) for i in sampled_inds_list])
    inds_normalised = [[x / image_size, y / image_size] for x, y in inds]
    return inds, inds_normalised