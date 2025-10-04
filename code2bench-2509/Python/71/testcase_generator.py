from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
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

# Strategy for generating token sequences
def token_sequence_strategy():
    return st.lists(
        st.lists(st.integers(min_value=0, max_value=100), min_size=0, max_size=10),
        min_size=1,
        max_size=10,
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    tokens_list=token_sequence_strategy(),
    max_duration=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
    prompt_duration=st.floats(min_value=0.1, max_value=10.0, allow_nan=False, allow_infinity=False),
    token_duration=st.floats(min_value=0.1, max_value=10.0, allow_nan=False, allow_infinity=False),
)
@example(tokens_list=[[1, 2, 3]], max_duration=10.0, prompt_duration=1.0, token_duration=1.0)
@example(tokens_list=[[1, 2], [3, 4, 5]], max_duration=5.0, prompt_duration=1.0, token_duration=1.0)
@example(tokens_list=[[1], [2], [3]], max_duration=10.0, prompt_duration=1.0, token_duration=1.0)
@example(tokens_list=[[1, 2, 3, 4, 5]], max_duration=1.0, prompt_duration=1.0, token_duration=1.0)
@example(tokens_list=[[], [1, 2]], max_duration=10.0, prompt_duration=1.0, token_duration=1.0)
def test_batchify_tokens(tokens_list, max_duration, prompt_duration, token_duration):
    global stop_collecting
    if stop_collecting:
        return

    tokens_list_copy = copy.deepcopy(tokens_list)
    try:
        batches, index = batchify_tokens(tokens_list_copy, max_duration, prompt_duration, token_duration)
    except Exception:
        return  # Skip inputs that cause exceptions

    generated_cases.append({
        "Inputs": {
            "tokens_list": tokens_list,
            "max_duration": max_duration,
            "prompt_duration": prompt_duration,
            "token_duration": token_duration,
        },
        "Expected": {
            "batches": batches,
            "index": index,
        }
    })
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)