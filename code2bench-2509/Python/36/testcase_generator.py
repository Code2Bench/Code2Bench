from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
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
def align_ampersands(str1, str2):
    """
    This function takes two strings containing various "&" characters and transforms them so that the indices of "&"
    are aligned. This is useful for formatting LaTeX tables.

    Args:
        str1 (str): First input string containing "&" characters.
        str2 (str): Second input string containing "&" characters.

    Returns:
        Tuple[str, str]: Two transformed strings with aligned "&" indices.
    """
    # Find indices of "&" characters in both strings
    amp_idx1 = [i for i, char in enumerate(str1) if char == "&"]
    amp_idx2 = [i for i, char in enumerate(str2) if char == "&"]

    assert len(amp_idx1) == len(amp_idx2)

    # Replace "&" characters in the strings with "\&" at the aligned indices
    acc1, acc2 = 0, 0
    for i, j in zip(amp_idx1, amp_idx2):
        diff = (j + acc2) - (i + acc1)
        if diff > 0:
            str1 = str1[: i + acc1] + " " * diff + str1[i + acc1 :]
            acc1 += diff
        elif diff < 0:
            str2 = str2[: j + acc2] + " " * (-diff) + str2[j + acc2 :]
            acc2 -= diff

    return str1, str2

# Strategy for generating strings with "&" characters
def ampersand_string_strategy():
    return st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), blacklist_characters="&"),
        min_size=0,
        max_size=20
    ).flatmap(
        lambda s: st.lists(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), blacklist_characters="&"), min_size=0, max_size=5),
            min_size=0,
            max_size=5
        ).map(
            lambda parts: "&".join(parts)
        )
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(str1=ampersand_string_strategy(), str2=ampersand_string_strategy())
@example(str1="a&b&c", str2="d&e&f")
@example(str1="a&b", str2="c&d")
@example(str1="a&b&c", str2="d&e")
@example(str1="a&b", str2="c&d&e")
@example(str1="a", str2="b")
@example(str1="", str2="")
def test_align_ampersands(str1, str2):
    global stop_collecting
    if stop_collecting:
        return
    
    # Ensure both strings have the same number of "&" characters
    amp_count1 = str1.count("&")
    amp_count2 = str2.count("&")
    if amp_count1 != amp_count2:
        return  # Skip inputs with mismatched "&" counts
    
    str1_copy = copy.deepcopy(str1)
    str2_copy = copy.deepcopy(str2)
    try:
        expected = align_ampersands(str1_copy, str2_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"str1": str1, "str2": str2},
        "Expected": expected
    })
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)