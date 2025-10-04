import numpy as np

def post_process_sampled_indices(*, sampled_inds_list, attn_map, image_size):
    inds = np.array(sampled_inds_list).flatten()
    inds = np.array(np.unravel_index(inds, attn_map.shape)).T

    inds_normalised = np.zeros(inds.shape)
    inds_normalised[:, 0] = inds[:, 1] / image_size
    inds_normalised[:, 1] = inds[:, 0] / image_size
    inds_normalised = inds_normalised.tolist()

    return inds, inds_normalised