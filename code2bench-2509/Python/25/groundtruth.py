

def split_token_counts_and_frame_ids(T, token_frame, world_size, rank):

    S = T * token_frame
    split_sizes = [S // world_size + (1 if i < S % world_size else 0) for i in range(world_size)]
    start = sum(split_sizes[:rank])
    end = start + split_sizes[rank]
    counts = [0] * T
    for idx in range(start, end):
        t = idx // token_frame
        counts[t] += 1

    counts_filtered = []
    frame_ids = []
    for t, c in enumerate(counts):
        if c > 0:
            counts_filtered.append(c)
            frame_ids.append(t)
    return counts_filtered, frame_ids