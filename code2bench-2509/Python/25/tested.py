from typing import List, Tuple

def split_token_counts_and_frame_ids(T: int, token_frame: int, world_size: int, rank: int) -> Tuple[List[int], List[int]]:
    total_frames = T * token_frame
    token_counts = []
    frame_ids = []
    
    # Calculate how many tokens each rank should get
    tokens_per_rank = total_frames // world_size
    remainder = total_frames % world_size
    
    # Calculate token counts for the specified rank
    token_counts.append(tokens_per_rank + (1 if rank < remainder else 0))
    
    # Calculate frame IDs for the specified rank
    frame_ids.append(rank)
    if rank < remainder:
        frame_ids.append(rank)
    
    return token_counts, frame_ids