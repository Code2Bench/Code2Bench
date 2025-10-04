from typing import List

def chunk_sentences(
    sentences: List[str], max_chunk_size: int, overlap_sentences: int
) -> List[str]:
    if not sentences:
        return []

    chunks = []
    current_chunk = []
    current_chunk_length = 0

    for i, sentence in enumerate(sentences):
        # Add the current sentence to the chunk
        current_chunk.append(sentence)
        current_chunk_length += len(sentence)

        # Check if the chunk exceeds the maximum size
        if current_chunk_length > max_chunk_size:
            # If overlap is greater than zero, include the last overlap sentences at the start of the next chunk
            if overlap_sentences > 0:
                chunks.append(''.join(current_chunk[-overlap_sentences:]))
                current_chunk = current_chunk[:-overlap_sentences]
                current_chunk_length = len(current_chunk) * len(current_chunk[0])  # This line is a placeholder and may need adjustment

            else:
                chunks.append(''.join(current_chunk))
                current_chunk = []
                current_chunk_length = 0

        # If we have reached the end of the list, add the remaining chunk
        if i == len(sentences) - 1:
            if current_chunk:
                chunks.append(''.join(current_chunk))

    return chunks