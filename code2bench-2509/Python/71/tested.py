from typing import List, Tuple

def batchify_tokens(
    tokens_list: List[List[int]],
    max_duration: float,
    prompt_duration: float,
    token_duration: float,
) -> Tuple[List[List[List[int]]], List[int]]:
    batches = []
    current_batch = []
    original_indices = []

    for i, seq in enumerate(tokens_list):
        # Calculate the total duration for the current sequence
        total_duration = prompt_duration + len(seq) * token_duration

        # Add the sequence to the current batch if it fits
        if total_duration <= max_duration:
            current_batch.append(seq)
            original_indices.append(i)
        else:
            # Finalize the current batch and start a new one
            batches.append(current_batch)
            current_batch = [seq]
            original_indices.append(i)

    # Add the last batch
    if current_batch:
        batches.append(current_batch)
        original_indices.append(i)

    return (batches, original_indices)