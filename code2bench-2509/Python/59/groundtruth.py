

def valid_cluster_shape(cc: int, cluster_shape: list) -> tuple:
    """
    Checks whether a device with `cc` supports a thread block cluster of shape `cluster_shape`.

    :param cc: compute capability of device in question
    :type cc: int
    :param cluster_shape: dimensions of thread block cluster shape to check
    :type cluster_shape: list

    :return: tuple with the first element indicating whether the provided cluster shape is
             valid for the provided device and the second element being an error message
    :rtype: tuple
    """

    if cc < 90:
        if cluster_shape != [1, 1, 1]:
            return (False,
                    f"Cluster shape for pre-SM90 architectures must be [1, 1, 1]. Received cluster shape of "
                    f"{cluster_shape} for SM{cc}.")
        else:
            return (True, "")

    if len(cluster_shape) != 3:
        return (False,
                f"Cluster shapes must be rank-3. Received {cluster_shape} (rank {len(cluster_shape)}")

    if cluster_shape[2] != 1:
        return (False,
                "CUTLASS kernels currently require the third dimension of cluster shape to be 1. "
                f"Received cluster shape of {cluster_shape}.")

    # The CUDA programming guide currently defines a maximum of 8 thread blocks per cluster
    # as being portably supported (https://docs.nvidia.com/cuda/cuda-c-programming-guide/#thread-block-clusters).
    # Current CUTLASS kernels only have non-unit cluster dimensions within the first two dimensions,
    # so we check that the first two dimensions of the cluster shape do not exceed 8 thread blocks in total.
    blocks_in_2d = cluster_shape[0] * cluster_shape[1]
    if blocks_in_2d > 8:
        return (False,
            f"Thread block clusters with more than 8 thread blocks are currently unsupported on SM{cc}. "
            f"Received cluster shape {cluster_shape}, which has {blocks_in_2d} thread blocks.")
    return (True, "")