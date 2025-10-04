from typing import Tuple, List

def valid_cluster_shape(cc: int, cluster_shape: List[int]) -> Tuple[bool, str]:
    if cc < 90:
        return (cluster_shape == [1, 1, 1], '')
    else:
        if not isinstance(cluster_shape, list):
            return (False, "Cluster shape must be a list.")
        if len(cluster_shape) != 3:
            return (False, "Cluster shape must be a 3-dimensional list.")
        if cluster_shape[2] != 1:
            return (False, "Third dimension of cluster shape must be 1.")
        if cluster_shape[0] * cluster_shape[1] > 8:
            return (False, "Product of first two dimensions of cluster shape must not exceed 8.")
        return (True, '')