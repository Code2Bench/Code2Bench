

def sample_indices(N, stride, expand_ratio, c):
    indices = []
    current_start = 0

    while current_start < N:
        bucket_width = int(stride * (expand_ratio**(len(indices) / stride)))

        interval = int(bucket_width / stride * c)
        current_end = min(N, current_start + bucket_width)
        bucket_samples = []
        for i in range(current_end - 1, current_start - 1, -interval):
            for near in range(c):
                bucket_samples.append(i - near)

        indices += bucket_samples[::-1]
        current_start += bucket_width

    return indices