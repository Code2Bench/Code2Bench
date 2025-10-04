from typing import List

def chunk_sentences(
    sentences: List[str], max_chunk_size: int, overlap_sentences: int
) -> List[str]:
    """
    Helper to group sentences into chunks with overlap.
    """
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sep = " " if current_chunk else ""
        new_length = current_length + len(sep) + len(sentence)
        if new_length > max_chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            overlap = current_chunk[-overlap_sentences:] if overlap_sentences else []
            current_chunk = overlap + [sentence]
            current_length = sum(len(s) for s in current_chunk) + len(current_chunk) - 1
        else:
            current_chunk.append(sentence)
            current_length = new_length
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks