from typing import List

def sample_indices(N: int, stride: int, expand_ratio: float, c: int) -> List[int]:
    # Initialize the list of indices
    indices = []
    
    # Calculate the initial bucket width
    bucket_width = stride
    
    # Calculate the current bucket width for each iteration
    current_bucket_width = stride
    
    # Calculate the number of buckets needed to cover the range [0, N)
    num_buckets = 1
    while current_bucket_width < N:
        num_buckets += 1
        current_bucket_width *= expand_ratio
    
    # Generate samples within each bucket
    for i in range(num_buckets):
        # Calculate the starting index of the current bucket
        start = i * current_bucket_width
        
        # Calculate the ending index of the current bucket
        end = start + current_bucket_width
        
        # Generate samples within the current bucket
        for j in range(start, end, current_bucket_width):
            # Add the sampled index to the list
            indices.append(j)
    
    return indices