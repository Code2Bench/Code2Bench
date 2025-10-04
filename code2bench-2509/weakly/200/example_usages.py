from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from collections import Counter
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "example_usages.json")
generated_cases = {
    "Normal cases": [],
    "Others": []
}
stop_collecting = False
case_count = 0
MAX_CASES = 8

# Ground truth function
def majority_vote_move(moves_list, prev_move=None):
    """
    Returns the majority-voted move from moves_list.
    If there's a tie for the top count, and if prev_move is among those tied moves,
    prev_move is chosen. Otherwise, pick the first move from the tie.
    """
    if not moves_list:
        return None

    c = Counter(moves_list)

    counts = c.most_common()
    top_count = counts[0][1]  # highest vote count

    tie_moves = [m for m, cnt in counts if cnt == top_count]

    if len(tie_moves) > 1 and prev_move:
        if prev_move in tie_moves:
            return prev_move
        else:
            return tie_moves[0]
    else:
        return tie_moves[0]

# Strategies for generating inputs
def moves_list_strategy():
    return st.lists(
        st.sampled_from(['rock', 'paper', 'scissors']),
        min_size=0, max_size=10
    )

def prev_move_strategy():
    return st.one_of(
        st.none(),
        st.sampled_from(['rock', 'paper', 'scissors'])
    )

# Hypothesis test configuration
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
@given(
    moves_list=moves_list_strategy(),
    prev_move=prev_move_strategy()
)
@example(moves_list=[], prev_move=None)
@example(moves_list=['rock'], prev_move=None)
@example(moves_list=['rock', 'rock', 'paper'], prev_move=None)
@example(moves_list=['rock', 'paper', 'scissors'], prev_move='rock')
@example(moves_list=['rock', 'paper', 'paper'], prev_move='rock')
@example(moves_list=['rock', 'rock', 'paper', 'paper'], prev_move='rock')
def test_majority_vote_move(moves_list, prev_move):
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
        return

    # Deep copy inputs to avoid modification
    moves_list_copy = copy.deepcopy(moves_list)
    prev_move_copy = copy.deepcopy(prev_move)

    # Call func0 to verify input validity
    try:
        expected = majority_vote_move(moves_list_copy, prev_move_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "Single move in the list"
        elif case_count == 1:
            desc = "Multiple moves with a clear majority"
        else:
            desc = "Tie with previous move influencing the result"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "Empty moves list"
        elif case_count == 4:
            desc = "Tie without previous move"
        elif case_count == 5:
            desc = "All moves tied"
        elif case_count == 6:
            desc = "Previous move not in tied moves"
        else:
            desc = "Multiple ties with previous move"

    # Store case
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {
            "moves_list": moves_list_copy,
            "prev_move": prev_move_copy
        },
        "Expected": expected,
        "Usage": None
    })
    case_count += 1
    if case_count >= MAX_CASES:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {sum(len(cases) for cases in generated_cases.values())} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)