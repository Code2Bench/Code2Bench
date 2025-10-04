from typing import List

def get_minimum_num_micro_batch_size(total_lengths: List[int], max_tokens_per_gpu: int) -> int:
    batches = []
    for length in total_lengths:
        placed = False
        for i in range(len(batches)):
            if batches[i] + length <= max_tokens_per_gpu:
                batches[i] += length
                placed = True
                break
        if not placed:
            batches.append(length)
    return len(batches)