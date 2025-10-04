from typing import List

def batchify_tokens(
    tokens_list: List[List[int]],
    max_duration: float,
    prompt_duration: float,
    token_duration: float,
):
    """
    Sort and group the input list of token sequences into batches, where each batch's
        total duration does not exceed the maximum.

    Args:
        tokens_list (List[List[int]]): A list of token sequences, where each inner
            list represents a sequence of tokens.
        max_duration (float): The maximum allowed total duration for each batch.
        prompt_duration (float): The duration cost per prompt in the batch.
        token_duration (float): The duration cost per token.

    Returns:
        batches: List[List[List[int]]]: A list of batches, where each batch is a list of
            token sequences that fit within the max duration.
        index: List[int]: The original index of each sentence, used to recover the
            sequential order in the future.
    """
    # Create index for each sentence
    indexed_tokens = list(enumerate(tokens_list))

    # Sort according to sentence length (for less padding)
    indexed_sorted_tokens = sorted(indexed_tokens, key=lambda x: len(x[1]))
    index = [indexed_sorted_tokens[i][0] for i in range(len(indexed_sorted_tokens))]
    sorted_tokens = [
        indexed_sorted_tokens[i][1] for i in range(len(indexed_sorted_tokens))
    ]

    batches = []
    batch = []
    batch_size = 0  # Total number of tokens in current batch

    for tokens in sorted_tokens:
        # Calculate if adding current token sequence would exceed max duration
        # Formula considers: existing tokens' duration + existing
        # prompts' duration + new tokens' duration
        if (
            batch_size * token_duration
            + len(batch) * prompt_duration
            + len(tokens) * token_duration
            <= max_duration
        ):
            # Add to current batch if within duration limit
            batch.append(tokens)
            batch_size += len(tokens)
        else:
            # If exceeding limit, finalize current batch (if not empty)
            if len(batch) > 0:
                batches.append(batch)
            # Start new batch with current token sequence
            batch = [tokens]
            batch_size = len(tokens)

    # Add the last batch if it's not empty
    if len(batch) > 0:
        batches.append(batch)

    return batches, index