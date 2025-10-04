from typing import List

def greedy_partition(seqlen_list: List[int], k_partitions: int, equal_size: bool) -> List[List[int]]:
    if equal_size and k_partitions * seqlen_list[0] % k_partitions != 0:
        raise AssertionError("Equal size partitions not possible")
    
    if equal_size:
        partition_size = len(seqlen_list) // k_partitions
        partitions = []
        for i in range(k_partitions):
            partitions.append(seqlen_list[i * partition_size : (i + 1) * partition_size])
        return partitions
    
    # Greedy algorithm to assign sequence lengths to partitions
    partitions = []
    current_sum = 0
    for i in range(len(seqlen_list)):
        if current_sum + seqlen_list[i] <= k_partitions * max(seqlen_list):
            current_sum += seqlen_list[i]
            partitions.append([seqlen_list[i]])
        else:
            partitions[-1].append(seqlen_list[i])
    
    return partitions