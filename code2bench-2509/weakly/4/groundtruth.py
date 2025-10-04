
import bisect

def find_chunk_index(chunks, idx):
    """
    Find the 0-based chunk index that contains the given index idx.
    chunks: List of (begin_idx, end_idx).
    idx: The index to search for.
    Returns the 0-based chunk index.
    """
    starts = [chunk[0] for chunk in chunks]
    pos = bisect.bisect_right(starts, idx) - 1  # Find position of idx in starts
    if pos < 0 or pos >= len(chunks):
        raise ValueError(f"Index {idx} not found in any chunk")
    chunk_begin, chunk_end = chunks[pos]
    if idx < chunk_begin or idx > chunk_end:
        raise ValueError(f"Index {idx} not found in any chunk")
    return pos